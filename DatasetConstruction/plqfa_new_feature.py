from urllib.parse import urlparse

def number_of_hashtags(url):
    """Counts the number of hashtags (#) in the URL."""
    return url.count('#')

def number_of_subdomains(url):
    """Counts the number of subdomains in the URL."""
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    if hostname:
        subdomains = hostname.split('.')
        if len(subdomains) > 2:
            return len(subdomains) - 2
        elif len(subdomains) == 2:
            return 0
        else:
            return 0
    return 0

def having_path(url):
    """Checks if the URL has a path."""
    parsed_url = urlparse(url)
    return 1 if parsed_url.path else 0

def path_length(url):
    """Calculates the length of the path in the URL."""
    parsed_url = urlparse(url)
    return len(parsed_url.path)

def having_query(url):
    """Checks if the URL has a query."""
    parsed_url = urlparse(url)
    return 1 if parsed_url.query else 0

def having_fragment(url):
    """Checks if the URL has a fragment."""
    parsed_url = urlparse(url)
    return 1 if parsed_url.fragment else 0

def having_anchor(url):
    """Checks if the URL has an anchor (fragment)."""
    return having_fragment(url) and 'a' in url

# def main():
#     url = input("Enter a URL: ").strip()
    
#     print(f"Number of hashtags in URL: {number_of_hashtags(url)}")
#     print(f"Number of subdomains: {number_of_subdomains(url)}")
#     print(f"Having path: {having_path(url)}")
#     print(f"Path length: {path_length(url)}")
#     print(f"Having query: {having_query(url)}")
#     print(f"Having fragment: {having_fragment(url)}")
#     print(f"Having anchor: {having_anchor(url)}")

# if __name__ == "__main__":
#     main()
