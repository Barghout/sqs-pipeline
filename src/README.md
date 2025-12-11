\# SQS Data Pipeline - LocalStack \& Postgres



\## Project Structure

```

sqs-pipeline/

├─ message\_generator.go       # Generates and sends messages to the local SQS queue

├─ etl.py                     # Reads messages from SQS and stores them in Postgres

├─ docker-compose.yml         # LocalStack and Postgres containers

├─ go.mod \& go.sum            # required for building the Go message generator

├─ DOC.md                     # Detailed documentation

└─ README.md                  # Project overview

```



\## Prerequisites

\- Docker \& Docker Compose

\- Go installed (for message generator)

\- Python 3.11+ with `boto3` and `psycopg2`

```bash

pip install boto3 psycopg2

```



\## Setup \& Run



1\. \*\*Start containers\*\*

```bash

docker-compose up -d

```

Starts LocalStack (SQS) and Postgres.



2\. \*\*Create SQS queue\*\*

```bash

aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name test-queue

```



3\. \*\*Generate messages\*\*

```bash

go run message\_generator.go

```



4\. \*\*Run ETL script\*\*

```bash

python etl.py

```



5. \*\*Viewing Data\*\*

```bash
docker exec -it sqs-pipeline-etl-postgres-1 psql -U postgres -d etl\_db


SELECT \* FROM messages;

```





This reads messages from SQS and stores them in Postgres, skipping malformed messages.



\## Database

\- Database: `etl\_db`

\- User: `postgres`

\- Password: `mypassword`

\- Table: `messages`

```sql

CREATE TABLE messages (

&nbsp;   id INT PRIMARY KEY,

&nbsp;   mail VARCHAR(255),

&nbsp;   name VARCHAR(255),

&nbsp;   surname VARCHAR(255),

&nbsp;   details JSONB

);

```


