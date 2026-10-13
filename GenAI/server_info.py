import requests
from urllib.parse import urlparse

# Function to extract server information for a given URL
def get_server_info(url):
    # Parse the domain from the given URL
    parsed_url = urlparse(url)
    domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
    
    try:
        # Send a request to the server
        response = requests.get(url, timeout=10)
        
        # Extract server information from response headers
        server_info = {
            'Server': response.headers.get('Server'),
            'X-Powered-By': response.headers.get('X-Powered-By'),
            'Content-Type': response.headers.get('Content-Type'),
            'Status Code': response.status_code
        }
        
        # Return the extracted server information
        return server_info
    except requests.RequestException as e:
        return f"Error fetching server info: {str(e)}"

# Example usage
if __name__ == "__main__":
    url = input("Enter a URL (format: https://www.example.com): ")
    server_info = get_server_info(url)
    print(server_info)
