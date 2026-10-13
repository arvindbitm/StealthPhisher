import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import pandas as pd

def get_url_features(url):
    features = {}

    parsed_url = urlparse(url)
    features['Protocol'] = parsed_url.scheme
    features['Domain'] = parsed_url.netloc
    features['Subdomain'] = '.'.join(parsed_url.netloc.split('.')[:-2]) if len(parsed_url.netloc.split('.')) > 2 else ''
    features['Path'] = parsed_url.path
    features['Query Parameters'] = parse_qs(parsed_url.query)
    features['Fragment'] = parsed_url.fragment

    try:
        response = requests.get(url)
        features['Status Code'] = response.status_code
        features['Response Time'] = response.elapsed.total_seconds()
        if response.status_code != 200:
            return features
        page_content = response.content
    except Exception as e:
        print(f"Error fetching the URL: {e}")
        return features

    soup = BeautifulSoup(page_content, 'lxml')

    features['Title'] = soup.title.string if soup.title else ''
    meta_description = soup.find('meta', attrs={'name': 'description'})
    features['Meta Description'] = meta_description['content'] if meta_description else ''
    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
    features['Keywords'] = meta_keywords['content'] if meta_keywords else ''
    features['Headings'] = {f'h{i}': [tag.get_text() for tag in soup.find_all(f'h{i}')] for i in range(1, 7)}
    features['Content Length'] = len(soup.get_text())
    features['Number of Images'] = len(soup.find_all('img'))
    features['Number of Links'] = len(soup.find_all('a'))

    features['Page Size'] = len(page_content)

    if parsed_url.scheme == 'https':
        try:
            import ssl
            ssl_info = ssl.get_server_certificate((parsed_url.netloc, 443))
            features['SSL Certificate Info'] = ssl_info
        except Exception as e:
            features['SSL Certificate Info'] = f"Error fetching SSL certificate: {e}"
    else:
        features['SSL Certificate Info'] = 'Not Applicable'

    features['Alt Text'] = [img.get('alt') for img in soup.find_all('img') if img.get('alt')]
    canonical_link = soup.find('link', attrs={'rel': 'canonical'})
    features['Canonical URL'] = canonical_link['href'] if canonical_link else ''
    features['Structured Data'] = [script.get_text() for script in soup.find_all('script', type='application/ld+json')]

    features['Open Graph Tags'] = {tag['property']: tag['content'] for tag in soup.find_all('meta') if tag.get('property', '').startswith('og:')}
    features['Twitter Cards'] = {tag['name']: tag['content'] for tag in soup.find_all('meta') if tag.get('name', '').startswith('twitter:')}

    features['Presence of Security Headers'] = {header: response.headers[header] for header in response.headers if header in ['Content-Security-Policy', 'X-Content-Type-Options']}
    features['Mixed Content'] = any(tag.get('src', '').startswith('http://') for tag in soup.find_all(['img', 'script']))

    features['Analytics Scripts'] = [script.get('src') for script in soup.find_all('script') if script.get('src') and 'analytics' in script.get('src')]
    features['Tracking Cookies'] = response.cookies.get_dict()

    features['Third-Party Scripts'] = [script['src'] for script in soup.find_all('script') if 'src' in script.attrs and parsed_url.netloc not in script['src']]
    features['Embedded Media'] = [media.get('src') for media in soup.find_all(['iframe', 'video', 'audio']) if media.get('src')]

    features['Forms'] = [{'action': form.get('action'), 'method': form.get('method')} for form in soup.find_all('form')]
    features['Interactive Elements'] = len(soup.find_all(['button', 'select', 'input', 'textarea']))

    return features

def display_features(features):
    df = pd.DataFrame(list(features.items()), columns=['Feature', 'Value'])
    print(df)


url = input("Enter a URL: ")
features = get_url_features(url)
display_features(features)
print("Thanks For Using...    See You Next Time......... ")