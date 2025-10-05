import aiohttp
import asyncio
from bs4 import BeautifulSoup
from chardet import detect  # Requires `chardet` library
from functools import lru_cache

# Asynchronous Fetching with aiohttp
async def fetch_links_async(url, limit=10, timeout=5):
    """Fetch links from a given URL asynchronously."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as response:
                # Detect encoding and decode the content
                raw_content = await response.content.read()
                encoding = detect(raw_content)['encoding']
                html = raw_content.decode(encoding if encoding else 'utf-8', errors='replace')
                soup = BeautifulSoup(html, 'html.parser')
                links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]
                return links[:limit]
    except Exception as e:
        print(f"Error fetching links from {url}: {e}")
        return []

# Caching Results with lru_cache
@lru_cache(maxsize=1000)
def shorten_url(url):
    """Shorten a URL for better readability."""
    from urllib.parse import urlparse
    parsed_url = urlparse(url)
    return f"{parsed_url.netloc}{parsed_url.path}"

# Count unique links using async processing
def count_unique_links(url, limit=10, timeout=5):
    """
    Fetch and count unique links from a given URL.
    """
    try:
        links = asyncio.run(fetch_links_async(url, limit, timeout))  # Use asyncio.run
        unique_urls = {shorten_url(link) for link in links}
        return len(unique_urls)
    except Exception as e:
        print(f"Error counting unique links for {url}: {e}")
        return 0  # Return 0 in case of an error

# # Main function for execution
# def main():
#     target_url = input("Enter the target URL: ").strip()
    
#     # Fetch and count unique links
#     unique_count = count_unique_links(target_url)
#     print(f"The number of unique links found on the page: {unique_count}")

# if __name__ == "__main__":
#     main()
