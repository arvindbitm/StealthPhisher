import dns.resolver
from urllib.parse import urlparse

# Function to get DNS records for a domain
def get_dns_records(domain):
    dns_info = {}
    try:
        # Get A record (IP address)
        try:
            a_records = dns.resolver.resolve(domain, 'A')
            dns_info['A Records'] = [record.to_text() for record in a_records]
        except dns.resolver.NoAnswer:
            dns_info['A Records'] = "No A records found"
        
        # Get MX records (Mail servers)
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            dns_info['MX Records'] = [record.to_text() for record in mx_records]
        except dns.resolver.NoAnswer:
            dns_info['MX Records'] = "No MX records found"
        
        # Get NS records (Name servers)
        try:
            ns_records = dns.resolver.resolve(domain, 'NS')
            dns_info['NS Records'] = [record.to_text() for record in ns_records]
        except dns.resolver.NoAnswer:
            dns_info['NS Records'] = "No NS records found"
        
        # Get TXT records (Text records)
        try:
            txt_records = dns.resolver.resolve(domain, 'TXT')
            dns_info['TXT Records'] = [record.to_text() for record in txt_records]
        except dns.resolver.NoAnswer:
            dns_info['TXT Records'] = "No TXT records found"
        
        return dns_info
    except Exception as e:
        return f"Error fetching DNS records: {str(e)}"
