import requests
import json

def check_url_safety(api_key, url_to_check):
    # Google Safe Browsing API endpoint
    endpoint = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    
    # Payload as per Google API documentation
    payload = {
        "client": {
            "clientId": "your-client-id",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["WINDOWS", "LINUX", "ANDROID", "IOS", "OSX"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url_to_check}
            ]
        }
    }
    
    # Sending a POST request to the API
    try:
        response = requests.post(endpoint, params={"key": api_key}, json=payload)
        response.raise_for_status()
        result = response.json()
        
        # Analyzing the result
        if "matches" in result:
            return f"Warning: The URL is unsafe! Threat details: {result['matches']}"
        else:
            return "The URL is safe!"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

