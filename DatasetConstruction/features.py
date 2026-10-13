# import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import whois
from datetime import datetime
from spellchecker import SpellChecker  # Changed import statement to use pyspellchecker


def get_features_from_html(html_content, url):
    features = {}
    soup = BeautifulSoup(html_content, 'html.parser')

    # URL features
    features['url_length'] = len(url)
    features['has_ip'] = urlparse(url).netloc.replace('.', '').isdigit()

    # Domain features
    parsed_url = urlparse(url)
    features['domain_age'] = get_domain_age(parsed_url.netloc)

    # Content features
    features['num_iframes'] = len(soup.find_all('iframe'))
    features['num_forms'] = len(soup.find_all('form'))
    features['num_hidden_fields'] = len(soup.find_all('input', type='hidden'))

    # Textual features
    text_content = soup.get_text()
    features['num_spelling_errors'] = get_spelling_errors(text_content)

    return features


def get_domain_age(domain):
    try:
        domain_info = whois.whois(domain)
        creation_date = domain_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        age = (datetime.now() - creation_date).days
        return age
    except:
        return 0


def get_spelling_errors(text):
    spell = SpellChecker()  # Using SpellChecker class from pyspellchecker
    words = text.split()
    misspelled = spell.unknown(words)
    return len(misspelled)


# Example usage
file_path = 'WEBs/800001.txt'
url = 'https://pub-58021b15a40e466fb3c40445b33be53f.r2.dev/index.html'

with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

features = get_features_from_html(html_content, url)
print(features)
