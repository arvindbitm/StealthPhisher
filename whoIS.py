import whois
from urllib.parse import urlparse

def get_whois_details(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    try:
        whois_info = whois.whois(domain)
        
        # If WHOIS info is available, return it as a dictionary
        return {
            'domain_name': whois_info.get('domain_name', 'Not provided'),
            'registrar': whois_info.get('registrar', 'Not provided'),
            'creation_date': whois_info.get('creation_date', 'Not provided'),
            'expiration_date': whois_info.get('expiration_date', 'Not provided'),
            'name_servers': whois_info.get('name_servers', 'Not provided')
        }
    except Exception as e:
        # In case of error, return a dictionary with default values
        return {
            'domain_name': 'Not provided',
            'registrar': 'Not provided',
            'creation_date': 'Not provided',
            'expiration_date': 'Not provided',
            'name_servers': 'Not provided',
            'Error': f"Error fetching WHOIS details: {str(e)}"
        }
