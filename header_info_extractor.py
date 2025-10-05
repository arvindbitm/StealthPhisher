import requests

# Function to extract response headers
def get_response_headers(url):
    try:
        response = requests.get(url)
        headers = {
            'Server': response.headers.get('Server', 'Not provided'),
            'X-Powered-By': response.headers.get('X-Powered-By', 'Not provided'),
            'Content-Type': response.headers.get('Content-Type', 'Not provided'),
            'Status Code': response.status_code,
        }
        return headers
    except requests.RequestException as e:
        # Return a dictionary with error details instead of a string
        return {
            'Server': 'Not provided',
            'X-Powered-By': 'Not provided',
            'Content-Type': 'Not provided',
            'Status Code': None,
            'Error': f"Error fetching headers: {str(e)}"
        }
