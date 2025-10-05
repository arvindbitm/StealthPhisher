import os
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import tldextract
import whois
import ssl
import re
from datetime import datetime
import socket
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


# Function to fetch HTML asynchronously
async def fetch_html(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            response.raise_for_status()
            return await response.text()
    except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError) as e:
        print(f"Error fetching the HTML for {url}: {e}")
        return None


# Function to extract domain features using whois
def extract_domain_features(domain):
    domain_info = {}
    try:
        whois_info = whois.whois(domain)
        if isinstance(whois_info.creation_date, list):
            creation_date = whois_info.creation_date[0]
        else:
            creation_date = whois_info.creation_date
        domain_info['domain_age'] = (datetime.now() - creation_date).days if creation_date else None
    except Exception as e:
        print(f"Error fetching WHOIS info for {domain}: {e}")
        domain_info['domain_age'] = None

    return domain_info


# Function to extract SSL features
def extract_ssl_features(domain):
    ssl_info = {}
    context = ssl.create_default_context()

    try:
        with socket.create_connection((domain, 443), timeout=10) as conn:
            with context.wrap_socket(conn, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                ssl_info['ssl_certificate'] = True if cert else False
    except Exception as e:
        print(f"Error fetching SSL certificate for {domain}: {e}")
        ssl_info['ssl_certificate'] = False

    return ssl_info


# Function to extract HTML features
def extract_html_features(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        features = {}

        # HTML Structure
        features['html_structure'] = str(soup)

        # Number of specific tags
        features['num_forms'] = len(soup.find_all('form'))
        features['num_scripts'] = len(soup.find_all('script'))
        features['num_iframes'] = len(soup.find_all('iframe'))
        features['num_links'] = len(soup.find_all('a'))
        features['num_images'] = len(soup.find_all('img'))

        # Meta tags
        meta_tags = {tag.attrs.get('name', '').lower(): tag.attrs.get('content', '') for tag in soup.find_all('meta')}
        features['meta_title'] = meta_tags.get('title', '')
        features['meta_description'] = meta_tags.get('description', '')
        features['meta_keywords'] = meta_tags.get('keywords', '')

        # Inline styles and scripts
        features['num_inline_styles'] = len(soup.find_all(style=True))
        features['num_inline_scripts'] = len(soup.find_all('script', type='text/javascript'))

        # Embedded content
        features['num_embedded_content'] = len(soup.find_all(['embed', 'object', 'video', 'audio']))

        return features
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return {}


# Function to extract HTTP headers
async def extract_http_headers(session, url):
    try:
        async with session.head(url, timeout=10) as response:
            return dict(response.headers)
    except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError) as e:
        print(f"Error fetching HTTP headers for {url}: {e}")
        return {}


# Function to extract JavaScript features
def extract_javascript_features(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        scripts = soup.find_all('script')
        js_code = ""
        for script in scripts:
            if script.string:
                js_code += script.string
        return {'javascript_code': js_code}
    except Exception as e:
        print(f"Error extracting JavaScript features: {e}")
        return {'javascript_code': ''}


# Main function to extract all features
async def extract_features(session, url):
    features = {}

    # Fetch HTML content
    html = await fetch_html(session, url)
    if html:
        # Extract HTML and JavaScript features
        features.update(extract_html_features(html))
        features.update(extract_javascript_features(html))

        # Extract Domain-related features
        domain_parts = tldextract.extract(url)
        domain = f"{domain_parts.domain}.{domain_parts.suffix}"

        with ThreadPoolExecutor() as executor:
            domain_features = await asyncio.get_event_loop().run_in_executor(executor, extract_domain_features, domain)
            ssl_features = await asyncio.get_event_loop().run_in_executor(executor, extract_ssl_features, domain)

        features.update(domain_features)
        features.update(ssl_features)

        # Extract HTTP Headers
        features['http_headers'] = await extract_http_headers(session, url)

    return features


# Asynchronous function to handle multiple URLs
async def process_urls(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [extract_features(session, url) for url in urls]
        return await asyncio.gather(*tasks)


# Example URLs
urls = ["http://multigrad.in", "http://rapydlaunch.com", "http://gla.ac.in"]

# Run the async function
features_list = asyncio.run(process_urls(urls))

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(features_list)

# Display the DataFrame


# Optionally, save the DataFrame to a CSV file
df.to_csv('phishing_analysis.csv', index=False)
