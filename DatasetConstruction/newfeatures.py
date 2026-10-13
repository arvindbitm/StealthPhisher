import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import whois
from datetime import datetime
from spellchecker import SpellChecker
import pandas as pd


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
    except Exception as e:
        print(f"Error retrieving domain age for {domain}: {e}")
        return 0


def get_spelling_errors(text):
    spell = SpellChecker()
    words = text.split()
    misspelled = spell.unknown(words)
    return len(misspelled)


def process_files_in_batches(file_paths, urls, batch_size=1000, output_csv='extracted_features.csv'):
    total_files = len(file_paths)

    for start in range(0, total_files, batch_size):
        end = min(start + batch_size, total_files)
        batch_file_paths = file_paths[start:end]
        batch_urls = urls[start:end]

        all_features = []

        for file_path, url in zip(batch_file_paths, batch_urls):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()

                features = get_features_from_html(html_content, url)
                features['file_path'] = file_path
                features['url'] = url
                all_features.append(features)

            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

        df_batch = pd.DataFrame(all_features)

        # Append to CSV file
        if not os.path.exists(output_csv):
            df_batch.to_csv(output_csv, index=False)
        else:
            df_batch.to_csv(output_csv, mode='a', header=False, index=False)

        print(f"Processed files {start + 1} to {end} out of {total_files}")


# Example usage
html_dir = 'WEBs/'  # Directory containing HTML files
url_file = 'urls.txt'  # File containing URLs corresponding to the HTML files

# Collect all HTML file paths
file_paths = [os.path.join(html_dir, file) for file in os.listdir(html_dir) if file.endswith('.txt')]

# Read URLs from the URL file with 'utf-8' encoding
with open(url_file, 'r', encoding='utf-8') as f:
    urls = f.read().splitlines()

# Ensure the number of file paths matches the number of URLs
assert len(file_paths) == len(urls), "Mismatch between number of files and URLs"

process_files_in_batches(file_paths, urls)
