import requests
from urllib.parse import urlparse
import socket

def get_ip_location(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
    
    try:
        ip_address = socket.gethostbyname(domain)
        api_url = f"https://ipapi.co/{ip_address}/json/"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            ip_info = response.json()
            location_info = {
                'IP Address': ip_address,
                'City': ip_info.get('city', 'Not provided'),
                'Region': ip_info.get('region', 'Not provided'),
                'Country': ip_info.get('country_name', 'Not provided'),
                'Latitude': ip_info.get('latitude', 'Not provided'),
                'Longitude': ip_info.get('longitude', 'Not provided'),
                'Org': ip_info.get('org', 'Not provided')
            }
            return location_info
        else:
            return {'IP Address': ip_address, 'Country': 'Not provided', 'City': 'Not provided'}

    except socket.gaierror:
        return {'IP Address': 'Not provided', 'Country': 'Not provided', 'City': 'Not provided'}
    except Exception as e:
        return {'IP Address': 'Not provided', 'Country': 'Not provided', 'City': 'Not provided'}

