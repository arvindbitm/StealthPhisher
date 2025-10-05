# safe_browsing_checker.py

import requests

def check_google_safe_browsing(url, api_key):
    """
    Checks a URL against the Google Safe Browsing API (v4).
    """
    if not api_key:
        return {"status": "SKIPPED", "details": "No API key provided."}

    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
    
    payload = {
        "client": {
            "clientId": "phishing-analyzer-tool",
            "clientVersion": "1.0.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }

    try:
        response = requests.post(api_url, json=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        
        if not result:
            return {"status": "SAFE", "details": "No threats found by Google Safe Browsing."}
        
        if 'matches' in result:
            return {"status": "UNSAFE", "details": result['matches']}
            
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
             return {"status": "ERROR", "details": "Permission Denied: Check if your API key is valid and has the Safe Browsing API enabled."}
        return {"status": "ERROR", "details": f"HTTP Error: {str(e)}"}
    except requests.exceptions.RequestException as e:
        return {"status": "ERROR", "details": f"A network error occurred: {str(e)}"}
    
    return {"status": "UNKNOWN", "details": "Could not determine the safety status."}