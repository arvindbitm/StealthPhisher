import sys
import networkx as nx
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import urllib.parse
import concurrent.futures
import os

# Use 'Agg' backend for environments where plots cannot be shown interactively
import matplotlib
matplotlib.use('Agg')

# Session object to reuse connections
session = requests.Session()

def fetch_links(url, limit=10, timeout=5):
    """Fetch links from a given URL."""
    try:
        response = session.get(url, timeout=timeout)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]
        return links[:limit]  # Limit the number of links fetched
    except Exception as e:
        print(f"Error fetching links from {url}: {e}")
        return []

def shorten_url(url):
    """Shorten and wrap long URLs for better readability."""
    parsed_url = urllib.parse.urlparse(url)
    short_url = f"{parsed_url.netloc}{parsed_url.path}"
    # Wrap long URLs every 30 characters
    return '\n'.join([short_url[i:i+30] for i in range(0, len(short_url), 30)])

def crawl(url, graph, visited, depth, max_depth, limit=10, timeout=5):
    """Crawl a given URL to a specified depth, building a graph of links."""
    if depth > max_depth or url in visited:
        return
    visited.add(url)  # Mark this URL as visited

    # Fetch links
    links = fetch_links(url, limit=limit, timeout=timeout)
    
    # Add links to the graph
    for link in links:
        graph.add_edge(shorten_url(url), shorten_url(link))

    # Process the next level of links in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(crawl, link, graph, visited, depth + 1, max_depth, limit, timeout) for link in links]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing link: {e}")

def get_domain_name(url):
    """Extract the domain name from the URL."""
    parsed_url = urllib.parse.urlparse(url)
    return parsed_url.netloc.replace('.', '_')  # Replace dots with underscores for filename safety

def plot_graph(graph, save_path):
    """Plot the graph of links using Matplotlib."""
    plt.figure(figsize=(20, 14))  # Increased figure size to accommodate long URLs
    pos = nx.spring_layout(graph, k=1, iterations=50)  # Adjust k for better spacing
    nx.draw(
        graph, 
        pos, 
        with_labels=True, 
        node_size=3000, 
        node_color="skyblue", 
        font_size=20,  # Increased font size
        font_weight="bold", 
        edge_color="gray", 
        font_color="black"
    )
    plt.savefig(save_path)  # Save the figure to a file
    print(f"Graph saved as {save_path}.")

# Main function to be called from the backend
def generate_site_map(url):
    # Initialize the graph and visited set
    graph = nx.DiGraph()
    visited = set()

    # Set max depth for crawling (avoid excessive depth)
    max_depth = 2

    # Start crawling and generate the graph
    crawl(url, graph, visited, depth=0, max_depth=max_depth, limit=5, timeout=5)

    # Define the save path using the domain name
    domain_name = get_domain_name(url)
    save_path = f"static/graphs/{domain_name}.png"

    # Plot the graph and save it
    plot_graph(graph, save_path)

    # Return the path to the saved graph image
    return save_path

# Script entry point when executed from the backend
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sitemapper.py <url>")
        sys.exit(1)
    url = sys.argv[1]  # Get the URL passed by backend
    graph_path = generate_site_map(url)  # Generate the site map and save the image
    print(graph_path)  # Output the graph path for integration with the Flask app
