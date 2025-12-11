# create_queue.py
from localstack_client.session import Session

session = Session()
sqs = session.client("sqs", endpoint_url="http://localhost:4566")

queue = sqs.create_queue(QueueName="my-queue")
print("Queue created:", queue['QueueUrl'])
