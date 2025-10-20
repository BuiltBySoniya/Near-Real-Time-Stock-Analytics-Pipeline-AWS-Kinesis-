# 🚀 Near Real-Time Stock Analytics Pipeline

Stream-processing stock market data with AWS serverless services

## Short Description

Built a near real-time analytics pipeline for stock market data using AWS. The system streams live stock quotes, computes metrics and anomalies via Lambda, stores structured results in DynamoDB, archives raw data in S3, enables querying via Athena, and sends alerts via SNS.

## 🛠️ AWS Services Used:

Amazon Kinesis Data Streams,
AWS Lambda,
Amazon DynamoDB,
Amazon S3,
Amazon Athena,
Amazon SNS,

## 🧰 Technical Tools:

Python (boto3, yfinance),
AWS CLI,
AWS SAM or CloudFormation (optional),
SQL in Athena,

## 🧠 Skills Demonstrated:

Streaming data ingestion and processing,
Real-time analytics & anomaly detection,
Serverless architecture and cost-optimization,
Historical data querying & alerting workflows,

## 📋 Steps Performed

### 1. Create Kinesis Data Stream

Established a Kinesis stream named `stock-market-stream` in “On-demand” mode for ingesting real-time stock data.

### 2. Set Up Local Python Environment & Producer Script

Installed Python 3.8+, boto3 and yfinance.
Ran a script that fetches stock prices (e.g., AAPL) every 30 seconds, computes change and change_percent, and sends JSON records to the Kinesis stream.

### 3. Configure AWS Lambda for Processing

Created a Lambda function triggered by the Kinesis stream with batch size 2.
Function decodes each record, stores raw data in S3 (`raw-data/...`), computes metrics (moving average, anomaly flag), and writes structured records to DynamoDB table `stock-market-data`.

### 4. Set Up Historical Data Store & Querying

Created DynamoDB table with partition key `symbol` and sort key `timestamp`.
Created S3 bucket to store raw data and created Glue Catalog / Athena table pointing to `s3://…/raw-data/`.
Queried sample data in Athena to compute price change or volume aggregates.

### 5. Configure Alerts via SNS

Enabled DynamoDB Streams on the `stock-market-data` table.
Created an SNS topic `Stock_Trend_Alerts`.
Deployed a second Lambda (`StockTrendAnalysis`) triggered by the stream, computing SMA-5/SMA-20 moving averages for each symbol and publishing BUY/SELL alerts when crossovers occur.

## ✅ Final Result:

A fully functional near-real-time stock analytics pipeline using AWS serverless services.

## 💼 Business Implication:

This project demonstrates how to build a cloud-native streaming analytics system capable of detecting trading signals and operational anomalies in near real time—empowering financial analysts and operations teams to respond quickly without the overhead of managing server infrastructure or complex workflows.
