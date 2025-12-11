# SQS Data Pipeline Documentation

## Overview
This ETL tool consumes messages from an AWS SQS queue (via LocalStack), converts them to a defined structure, and stores them in a local PostgreSQL database. Malformed messages are skipped.

## Project Structure
```
sqs-pipeline/
├─ message_generator.go       # Generates and sends messages to the local SQS queue
├─ etl.py                     # Reads messages from SQS and stores them in Postgres
├─ docker-compose.yml         # LocalStack and Postgres containers
├─ go.mod & go.sum            # Required for building the Go message generator
├─ README.md                  # Project overview
├─ DOCUMENTATION.md           # This documentation file
└─ run.ps1                    # Single command to run the full pipeline
```

## Prerequisites
- Docker & Docker Compose
- Go installed (for message generator)
- Python 3.11+ with `boto3` and `psycopg2`
```bash
pip install boto3 psycopg2
```

## Setup & Run

** single-command execution (Windows PowerShell)**
```powershell
.\run.ps1
```
Alternative way to run

1. **Start containers**
```powershell
docker-compose up -d
```
This starts LocalStack (for SQS) and PostgreSQL.

2. **Create SQS queue**
```powershell
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name test-queue
```

3. **Generate messages**
```powershell
go run message_generator.go
```

4. **Run ETL script**
```powershell
python etl.py
```


This runs all previous steps automatically.

## Viewing Data
```powershell
docker exec -it sqs-pipeline-etl-postgres-1 psql -U postgres -d etl_db
SELECT * FROM messages;
```

## Database
- Database: `etl_db`
- User: `postgres`
- Password: `mypassword`
- Table: `messages`
```sql
CREATE TABLE messages (
    id INT PRIMARY KEY,
    mail VARCHAR(255),
    name VARCHAR(255),
    surname VARCHAR(255),
    details JSONB
);
```

## Event Structure (Output Format)
```json
{
    "id": 1,
    "mail": "aaa@gmail.com",
    "name": "AAA SSS",
    "trip": {
        "depaure": "A",
        "destination": "D",
        "start_date": "2022-10-10 12:15:00",
        "end_date": "2022-10-10 13:55:00"
    }
}
```

## Notes
- The folder contains supporting Go module files (`go.mod` and `go.sum`) required for building the Go message generator.
- Malformed messages are automatically skipped.
- `run.ps1` allows running the full pipeline with a single command.
- Any database errors may require checking if the table `messages` exists.
- Adjust `region_name` in `etl.py` if necessary.

## Challenges
- Mapping different event structures to a single unified format.
- Ensuring the ETL can be run multiple times without duplicating data.
- Skipping malformed messages without breaking the pipeline.
- Integrating LocalStack for local SQS simulation.

## Bonus
- PostgreSQL database is included in `docker-compose.yml` for reproducibility.
- `run.ps1` provides a one-command execution for convenience.

