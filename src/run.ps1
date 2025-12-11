$ErrorActionPreference = "Stop"

Write-Host "Starting LocalStack and Postgres containers..."
docker-compose up -d

Start-Sleep -Seconds 5

Write-Host "Creating SQS queue 'test-queue'..."
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name test-queue

Write-Host "Generating messages..."
go run .\message_generator.go

Write-Host "Running ETL script..."
python .\etl.py

Write-Host "All done! Messages should now be in Postgres."
