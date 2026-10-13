import re

def detect_hexadecimal(url):
    hex_pattern = r'\b[0-9a-fA-F]{2,}\b'
    hex_matches = re.findall(hex_pattern, url)
    return len(hex_matches)

if __name__ == "__main__":
    url = input("Enter the URL for Hexadecimal pattern detection: ")
    result = detect_hexadecimal(url)
    print(f"Number of Hexadecimal patterns detected: {result}")
