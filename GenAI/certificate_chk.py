import ssl
import socket
import OpenSSL
def get_ssl_info(domain):
    """Extracts SSL certificate information for a domain."""
    try:
        # Connect to the server and get SSL certificate
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert_der = ssock.getpeercert(True)
                x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, cert_der)
                
                # Use decode() to convert bytes to string for JSON serialization
                issuer = {key.decode('utf-8'): val.decode('utf-8') for key, val in x509.get_issuer().get_components()}
                subject = {key.decode('utf-8'): val.decode('utf-8') for key, val in x509.get_subject().get_components()}

                cert_info = {
                    "Issuer": issuer,
                    "Subject": subject,
                    "Valid_From": x509.get_notBefore().decode('utf-8'),
                    "Valid_To": x509.get_notAfter().decode('utf-8'),
                    "Serial_Number": x509.get_serial_number()
                }
                return cert_info
    except Exception as e:

        return {"error": f"Error fetching SSL info: {str(e)}"}
