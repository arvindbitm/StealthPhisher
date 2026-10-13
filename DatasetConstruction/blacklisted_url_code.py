import requests

def check_url_safety(url):
    api_key = "A1B2C3D4E5F6G7H8I9J0"
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
    payload = {
        "client": {
            "clientId": "your_client_id",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["WINDOWS"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(api_url, json=payload, headers=headers)
    response_json = response.json()
    if "matches" in response_json:
        return "blacklisted"
    else:
        return "safe"

url = input("Enter a URL: ")
result = check_url_safety(url)
print(f"{url} is {result}")