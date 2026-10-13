import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
import concurrent.futures
import urllib.parse

def fetch_links(url, limit=10, timeout=5):
    """Fetch links from a given URL."""
    try:
        response = requests.get(url, timeout=timeout)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]
        return links[:limit]  # Limit the number of links fetched
    except Exception as e:
        print(f"Error fetching links from {url}: {e}")
        return []

def shorten_url(url):
    """Shorten a URL for better readability in the graph."""
    parsed_url = urllib.parse.urlparse(url)
    return f"{parsed_url.netloc}{parsed_url.path}"

def crawl(url, graph, depth, max_depth, unique_urls, limit=10, timeout=5):
    """Crawl a given URL to a specified depth, building a graph of links."""
    if depth > max_depth:
        return

    # Fetch links in parallel
    links = fetch_links(url, limit=limit, timeout=timeout)

    # Add links to the graph and track unique URLs
    for link in links:
        short_url = shorten_url(link)
        if short_url not in unique_urls:
            unique_urls.add(short_url)
            graph.add_edge(shorten_url(url), short_url)

    # Process the next level of links in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(crawl, link, graph, depth + 1, max_depth, unique_urls, limit, timeout) for link in links]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing link: {e}")

def plot_graph(graph, start_url):
    """Plot the graph of links using Matplotlib."""
    plt.figure(figsize=(14, 10))

    # Apply a spring layout with increased spacing
    pos = nx.spring_layout(graph, k=0.5, center=(0, 0), iterations=100)

    # Draw edges with arrows to show direction
    nx.draw_networkx_edges(graph, pos, alpha=0.6, edge_color="gray", arrows=True, arrowstyle="-|>", arrowsize=15)

    # Draw nodes with smaller sizes
    nx.draw_networkx_nodes(graph, pos, node_size=800, node_color="skyblue", alpha=0.9)

    # Draw labels with smaller font size for better spacing
    nx.draw_networkx_labels(graph, pos, font_size=8, font_weight="bold", font_color="black")

    # Title and display settings
    plt.title(f"Link Graph for {start_url}")
    plt.axis('off')
    plt.show()

# Parameters
start_url = input("Enter the URL ( use https://<url>.com format): ")  # Replace with the starting URL provided by the user
max_depth = 2  # Set a lower depth limit to prevent overload

# Initialize the graph and a set to track unique URLs
graph = nx.DiGraph()  # Make sure to use DiGraph for directed graphs
unique_urls = set()

# Start crawling
print("Crawling the website...")
crawl(start_url, graph, depth=0, max_depth=max_depth, unique_urls=unique_urls, limit=5, timeout=5)

# Plot the resulting graph
plot_graph(graph, shorten_url(start_url))

# Output the unique URLs and their count
print(f"\nTotal unique URLs found: {len(unique_urls)}")
print("Unique URLs:")
for url in unique_urls:
    print(url)