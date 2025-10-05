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

def crawl(url, graph, depth, max_depth, limit=10, timeout=5):
    """Crawl a given URL to a specified depth, building a graph of links."""
    if depth > max_depth:
        return
    
    # Fetch links in parallel
    links = fetch_links(url, limit=limit, timeout=timeout)
    
    # Add links to the graph
    for link in links:
        graph.add_edge(shorten_url(url), shorten_url(link))

    # Process the next level of links in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(crawl, link, graph, depth + 1, max_depth, limit, timeout) for link in links]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing link: {e}")

def plot_graph(graph):
    """Plot the graph of links using Matplotlib."""
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(graph, k=0.1)  # Adjust k for better spacing
    nx.draw(graph, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=8, font_weight="bold", edge_color="gray", font_color="black")
    plt.show()

# Parameters
start_url = input("enter the url: ")  # Replace with the starting URL provided by the user
max_depth = 2  # Set a lower depth limit to prevent overload

# Initialize the graph
graph = nx.DiGraph()

# Start crawling
crawl(start_url, graph, depth=0, max_depth=max_depth, limit=5, timeout=5)

# Plot the resulting graph
plot_graph(graph)
