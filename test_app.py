import requests

# Define the API endpoint and payload
url = "http://127.0.0.1:5000/predict"
payload = {
    "coin": "BTC",
    "time_period": 180  # 1440 minutes = 1 day
}

# Send a POST request to the API
response = requests.post(url, json=payload)

# Check the response
if response.status_code == 200:
    print("API Response:", response.json())
else:
    print("Failed to get a valid response. Status code:", response.status_code)

