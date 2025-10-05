import requests

# Function to extract response headers
def get_response_headers(url):
    try:
        response = requests.get(url)
        headers = response.headers
        return headers
    except requests.RequestException as e:
        return f"Error fetching headers: {str(e)}"

# Example usage
if __name__ == "__main__":
    url = input("Enter a URL (format: https://www.example.com): ")
    headers = get_response_headers(url)
    print(headers)
