import sys
from playwright.sync_api import sync_playwright
import urllib.parse
import os

def capture_screenshot(url, output_dir="static/screenshots"):
    # Extract domain name from URL
    parsed_url = urllib.parse.urlparse(url)
    domain_name = parsed_url.netloc.replace('.', '_')  # Replace dots with underscores for safe file names

    # Define the output file name
    output_file = f"{output_dir}/{domain_name}.png"

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Start playwright and open the browser
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Open the given URL
        page.goto(url)

        # Take a screenshot and save it to the specified file
        page.screenshot(path=output_file)
        print(f"Screenshot saved as {output_file}")

        # Close the browser
        browser.close()

    return output_file  # Return the saved screenshot file path

# Main function to get arguments from command line
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python screenshot.py <url>")
        sys.exit(1)

    url = sys.argv[1]  # The URL from command line
    capture_screenshot(url)
