
import requests
import time

# Setup headers (very important)
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "application/json",
    "Referer": "https://www.nseindia.com",
    "Connection": "keep-alive"
}

# Use a session to retain cookies
session = requests.Session()
session.headers.update(headers)

# Step 1: Visit homepage to get cookies set
# session.get("https://www.nseindia.com", timeout=5)
# time.sleep(1)

# Step 2: Hit the Nifty 50 stocks endpoint
url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"
response = session.get(url, timeout=5)

# Step 3: Extract and print stock names
if response.status_code == 200:
    data = response.json()
    nifty_stocks = data["data"]
    for stock in nifty_stocks:
        print(f"{stock['symbol']} - {stock['identifier']} ")
        if stock['symbol'] != 'NIFTY 50':
            with open('market/Nifty50Stocks.txt','a') as file:
                file.write(f"{stock['symbol']} - {stock['identifier']}:")
else:
    print("Error:", response.status_code)
    print(response.text[:300])
