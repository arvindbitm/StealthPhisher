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
            'Server': response.headers.get('Server', 'Not provided'),
            'X-Powered-By': response.headers.get('X-Powered-By', 'Not provided'),
            'Content-Type': response.headers.get('Content-Type', 'Not provided'),
            'Status Code': response.status_code
        }
        return server_info
    except requests.RequestException as e:
        # Return a dictionary with error details instead of a string
        return {
            'Server': 'Not provided',
            'X-Powered-By': 'Not provided',
            'Content-Type': 'Not provided',
            'Status Code': None,
            'Error': f"Error fetching server info: {str(e)}"
        }
