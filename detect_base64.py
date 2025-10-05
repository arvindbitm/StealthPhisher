import re

def detect_base64(url):
    base64_pattern = r'\b[A-Za-z0-9+/]{4,}={0,2}\b'
    base64_matches = re.findall(base64_pattern, url)
    return len(base64_matches)

if __name__ == "__main__":
    url = input("Enter the URL for Base64 pattern detection: ")
    result = detect_base64(url)
    print(f"Number of Base64 patterns detected: {result}")
