import whois

def get_whois_details(domain):
    """Gets WHOIS information for a given domain."""
    try:
        whois_info = whois.whois(domain)
        
        # Convert datetime objects to strings if they exist
        if whois_info.creation_date:
            creation_date = whois_info.creation_date[0].isoformat() if isinstance(whois_info.creation_date, list) else whois_info.creation_date.isoformat()
        else:
            creation_date = "Not provided"

        if whois_info.expiration_date:
            expiration_date = whois_info.expiration_date[0].isoformat() if isinstance(whois_info.expiration_date, list) else whois_info.expiration_date.isoformat()
        else:
            expiration_date = "Not provided"

        return {
            'domain_name': whois_info.domain_name,
            'registrar': whois_info.registrar,
            'creation_date': creation_date,
            'expiration_date': expiration_date,
            'name_servers': whois_info.name_servers
        }
    except Exception as e:
        return {"error": f"Could not retrieve WHOIS info: {str(e)}"}