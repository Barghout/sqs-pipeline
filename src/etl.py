import boto3
import psycopg2
import json

# --- SQS Setup ---
sqs = boto3.client(
    'sqs',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1'
)

queue_url = 'http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/test-queue'

# --- Database Setup ---
conn = psycopg2.connect(
    host='localhost',
    database='etl_db',  
    user='postgres',
    password='mypassword'
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INT PRIMARY KEY,
    mail TEXT,
    name TEXT,
    surname TEXT,
    details JSONB
)
""")
conn.commit()

# --- Read and process messages ---
while True:
    resp = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=2
    )
    messages = resp.get('Messages', [])
    if not messages:
        break

    for msg in messages:
        body_str = msg.get('Body')
        if not body_str:
            print("Skipping empty message")
            sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=msg['ReceiptHandle'])
            continue

        try:
            body = json.loads(body_str)
        except json.JSONDecodeError:
            print(f"Skipping malformed message: {body_str}")
            sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=msg['ReceiptHandle'])
            continue

        message_record = {
            'id': body.get('id'),
            'mail': body.get('mail'),
            'name': body.get('name'),
            'surname': body.get('surname'),
            'details': json.dumps(body.get('route') or body.get('locations') or body)
        }

        cur.execute("""
            INSERT INTO messages (id, mail, name, surname, details)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (
            message_record['id'],
            message_record['mail'],
            message_record['name'],
            message_record['surname'],
            message_record['details']
        ))

        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=msg['ReceiptHandle'])

conn.commit()
cur.close()
conn.close()

print("Completed")
