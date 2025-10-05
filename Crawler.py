import os
import sys
import time
import requests

def crawl_website(url):
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
    return response.text

def save_to_file(file_name, content):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)

def main():
    if len(sys.argv) != 2:
        print("Usage: python crawler.py <URL>")
        return

    url = sys.argv[1]
    output_folder = "WEBS"

    try:
        # Create the output directory if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Perform the crawl
        web_content = crawl_website(url)

        # Generate a unique numeric ID based on current timestamp
        numeric_id = str(int(time.time() * 1000))

        # Create the file name with only the numeric ID
        file_name = os.path.join(output_folder, f"{numeric_id}.txt")

        # Prepare the content with the ID and URL on the first line
        content = f"{numeric_id} {url}\n{web_content}"

        # Save the crawled content to the file
        save_to_file(file_name, content)

        print(f"Crawling completed. Saved to: {file_name}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
