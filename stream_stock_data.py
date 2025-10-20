import boto3
import json
import time
import yfinance as yf

# AWS Kinesis Configuration
kinesis_client = boto3.client("kinesis", region_name="us-east-1")
STREAM_NAME = "stock-market-stream"  # Replace with your actual stream name
STOCK_SYMBOL = "AAPL"
DELAY_TIME = 30  # seconds

def get_stock_data(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="2d")  # need 2 days to compute previous close

        if len(data) < 2:
            raise ValueError("Insufficient data to fetch previous close.")

        stock_data = {
            "symbol": symbol,
            "open": round(float(data.iloc[-1]["Open"]), 2),
            "high": round(float(data.iloc[-1]["High"]), 2),
            "low": round(float(data.iloc[-1]["Low"]), 2),
            "price": round(float(data.iloc[-1]["Close"]), 2),
            "previous_close": round(float(data.iloc[-2]["Close"]), 2),
            "change": round(float(data.iloc[-1]["Close"] - data.iloc[-2]["Close"]), 2),
            "change_percent": round(
                (float(data.iloc[-1]["Close"] - data.iloc[-2]["Close"]) / float(data.iloc[-2]["Close"])) * 100, 2
            ),
            "volume": int(data.iloc[-1]["Volume"]),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        return stock_data
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None

def send_to_kinesis():
    while True:
        try:
            stock_data = get_stock_data(STOCK_SYMBOL)
            if stock_data is None:
                print("Skipping this iteration due to data/API error.")
                time.sleep(DELAY_TIME)
                continue

            print(f"Sending: {stock_data}")

            resp = kinesis_client.put_record(
                StreamName=STREAM_NAME,
                Data=json.dumps(stock_data).encode("utf-8"),  # Kinesis expects BYTES
                PartitionKey=STOCK_SYMBOL,
            )

            if resp.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
                print(f"Kinesis Response: {resp}")
            else:
                print(f"Error sending to Kinesis: {resp}")

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(DELAY_TIME)

if __name__ == "__main__":
    send_to_kinesis()