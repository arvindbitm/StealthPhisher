import ssl
import socket
from urllib.parse import urlparse
import OpenSSL

# Function to extract SSL certificate information
def get_ssl_info(url):
    # Parse the domain from the given URL
    parsed_url = urlparse(url)
    domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
    
    try:
        # Connect to the server and get SSL certificate
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert(True)
                x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, cert)
                
                cert_info = {
                    "Issuer": dict(x509.get_issuer().get_components()),
                    "Subject": dict(x509.get_subject().get_components()),
                    "Valid From": x509.get_notBefore().decode('utf-8'),
                    "Valid To": x509.get_notAfter().decode('utf-8')
                }
                return cert_info
    except Exception as e:
        return f"Error fetching SSL info: {str(e)}"

# Example usage
if __name__ == "__main__":
    url = input("Enter a URL (format: https://www.example.com): ")
    ssl_info = get_ssl_info(url)
    print(ssl_info)
