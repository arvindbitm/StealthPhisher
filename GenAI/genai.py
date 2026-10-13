# genai.py (Updated and Corrected)

import os
from urllib.parse import urlparse
import networkx as nx
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER

# Import your existing modules
from certificate_chk import get_ssl_info
from dns_resolver import get_dns_records
from header_info_extractor import get_response_headers
from ip_loc import get_ip_location
from server_info import get_server_info
from whoIS import get_whois_details
from analyze_with_ai import analyze_with_ai
from site_mapper import crawl, shorten_url

# Import the new module
from safe_browsing_checker import check_google_safe_browsing

def generate_sitemap_image(start_url, max_depth=1, limit=5, timeout=5):
    """
    Crawls a website and generates a sitemap graph image.
    Returns the path to the saved image.
    """
    print("Generating sitemap visualization...")
    graph = nx.DiGraph()
    unique_urls = set()
    image_path = "sitemap.png"

    try:
        # Start crawling
        crawl(start_url, graph, depth=0, max_depth=max_depth, unique_urls=unique_urls, limit=limit, timeout=timeout)

        if not graph.nodes:
            print("Could not generate a sitemap. The graph is empty.")
            return None

        # Plot the graph
        plt.figure(figsize=(14, 10))
        pos = nx.spring_layout(graph, k=0.6, iterations=50)
        
        nx.draw_networkx_edges(graph, pos, alpha=0.6, edge_color="gray", arrows=True, arrowstyle="-|>", arrowsize=15)
        nx.draw_networkx_nodes(graph, pos, node_size=800, node_color="skyblue", alpha=0.9)
        nx.draw_networkx_labels(graph, pos, font_size=8, font_weight="bold", font_color="black")
        
        plt.title(f"Sitemap for {shorten_url(start_url)}")
        plt.axis('off')
        
        # Save the plot to a file
        plt.savefig(image_path, format='png', bbox_inches='tight')
        plt.close() # Close the plot to free up memory
        print(f"Sitemap image saved to {image_path}")
        return image_path
    except Exception as e:
        print(f"An error occurred during sitemap generation: {e}")
        return None


def create_pdf_report(url, sitemap_image_path, analysis_text):
    """
    Generates a PDF report with the sitemap image and AI analysis.
    """
    report_filename = "phishing_report.pdf"
    doc = SimpleDocTemplate(report_filename)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        name='Title',
        parent=styles['h1'],
        fontSize=24,
        leading=28,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    heading_style = styles['h2']
    body_style = ParagraphStyle(
        name='BodyText',
        parent=styles['Normal'],
        spaceAfter=12,
        leading=16
    )

    story = []

    # 1. Title
    story.append(Paragraph(f"Phishing Risk Report", title_style))
    story.append(Paragraph(f"URL Analyzed: {url}", styles['h3']))
    story.append(Spacer(1, 0.5 * inch))

    # 2. Sitemap Result
    story.append(Paragraph("Sitemap Visualization", heading_style))
    story.append(Spacer(1, 0.2 * inch))
    
    if sitemap_image_path and os.path.exists(sitemap_image_path):
        # Resize image to fit the page width if necessary
        img = Image(sitemap_image_path, width=7*inch, height=5*inch)
        img.hAlign = 'CENTER'
        story.append(img)
    else:
        story.append(Paragraph("Sitemap could not be generated.", body_style))
        
    story.append(PageBreak())

    # 3. Full Analysis from AI
    story.append(Paragraph("Full AI Analysis", heading_style))
    story.append(Spacer(1, 0.2 * inch))

    # Format the analysis text for the PDF
    formatted_analysis = analysis_text.replace('\n', '<br/>')
    story.append(Paragraph(formatted_analysis, body_style))

    # Build the PDF
    doc.build(story)
    print(f"\nReport successfully generated: {report_filename}")


def collect_data(url, api_key=None):
    """Collects all necessary information for a given URL."""
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if not domain:
            parsed_url = urlparse(f"http://{url}")
            domain = parsed_url.netloc
            url = parsed_url.geturl()
    except Exception as e:
        print(f"Error parsing URL: {e}")
        return None

    # --- Data Collection ---
    print("\nCollecting technical data...")
    data = {
        "URL": url,
        "Google_Safe_Browsing": check_google_safe_browsing(url, api_key),
        "Server_Info": get_server_info(url),
        "IP_Location": get_ip_location(url),
        "WHOIS_Details": get_whois_details(domain),
        "DNS_Records": get_dns_records(domain),
        "SSL_Certificate_Info": get_ssl_info(domain),
        "Response_Headers": dict(get_response_headers(url)),
    }
    return data

def main():
    """Main function to run the analysis and generate the PDF report."""
    # Ask for the Google Safe Browsing API key
    api_key = input("Enter your Google Safe Browsing API key (or press Enter to skip): ").strip()
    if not api_key:
        print("Google Safe Browsing check will be skipped.")

    url_input = input("Enter a URL to analyze (e.g., example.com): ")
    
    # Ensure URL has a scheme for requests
    if not url_input.startswith(('http://', 'https://')):
        url_input = 'https://' + url_input

    # 1. Generate Sitemap Image
    sitemap_path = generate_sitemap_image(url_input)

    # 2. Collect textual data, now with the API key
    data = collect_data(url_input, api_key)

    if data:
        # 3. Analyze with AI
        print("Data collected. Analyzing with AI...")
        report_text = analyze_with_ai(data)
        
        # 4. Create PDF Report
        print("Generating PDF report...")
        create_pdf_report(url_input, sitemap_path, report_text)
    else:
        print("Could not collect data. Aborting report generation.")

if __name__ == "__main__":
    main()