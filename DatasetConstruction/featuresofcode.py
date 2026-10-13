import requests
from bs4 import BeautifulSoup
import tldextract
import whois
import ssl
import http.client
from datetime import datetime
import socket
import re


def fetch_html(url):
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        print(f"Error fetching the HTML: {e}")
        return None


def extract_domain_features(url):
    domain_info = {}
    domain_parts = tldextract.extract(url)
    domain = f"{domain_parts.domain}.{domain_parts.suffix}"

    try:
        whois_info = whois.whois(domain)
        if whois_info.creation_date:
            domain_info['domain_age'] = (datetime.now() - whois_info.creation_date).days
        else:
            domain_info['domain_age'] = None
    except Exception as e:
        print(f"Error fetching WHOIS info: {e}")
        domain_info['domain_age'] = None

    return domain_info


def extract_ssl_features(url):
    ssl_info = {}
    domain_parts = tldextract.extract(url)
    domain = f"{domain_parts.domain}.{domain_parts.suffix}"

    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                ssl_info['ssl_certificate'] = True if cert else False
    except Exception as e:
        print(f"Error fetching SSL certificate: {e}")
        ssl_info['ssl_certificate'] = False

    return ssl_info


def extract_html_features(html):
    soup = BeautifulSoup(html, 'html.parser')
    features = {
        'num_forms': len(soup.find_all('form')),
        'num_scripts': len(soup.find_all('script')),
        'num_iframes': len(soup.find_all('iframe')),
        'num_links': len(soup.find_all('a')),
        'num_images': len(soup.find_all('img')),
        'meta_tags': {tag.attrs.get('name', '').lower(): tag.attrs.get('content', '') for tag in soup.find_all('meta')}
    }
    return features


def extract_http_headers(url):
    parsed_url = tldextract.extract(url)
    conn = http.client.HTTPSConnection(parsed_url.registered_domain)
    conn.request("HEAD", "/")
    res = conn.getresponse()
    headers = res.getheaders()
    return headers


def check_xss_vulnerability(html):
    patterns = [
        r"<script.*?>.*?</script.*?>",  # Embedded scripts
        r"on\w+\s*=\s*['\"].*?['\"]",  # Inline event handlers
    ]
    return any(re.search(pattern, html, re.IGNORECASE) for pattern in patterns)


def extract_meta_tags(soup):
    meta_tags = soup.find_all('meta')
    return {meta.attrs.get('name', ''): meta.attrs.get('content', '') for meta in meta_tags if 'name' in meta.attrs}


def extract_features(url):
    features = {}

    # Fetch HTML content
    html = fetch_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')

        # Extract HTML and JavaScript features
        features.update(extract_html_features(html))

        # Check for XSS vulnerabilities
        features['xss_vulnerable'] = check_xss_vulnerability(html)

        # Extract meta tags
        features['meta_tags'] = extract_meta_tags(soup)

        # Extract Domain-related features
        features.update(extract_domain_features(url))

        # Extract SSL features
        features.update(extract_ssl_features(url))

        # Extract HTTP Headers
        features['http_headers'] = extract_http_headers(url)

    return features


# Example URL to analyze
url = input("Enter the URL: ")
features = extract_features(url)
print(features)
