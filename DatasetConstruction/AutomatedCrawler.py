import os
import requests
import zipfile
from datetime import datetime

class AutomatedCrawler:
    def __init__(self, url):
        self.url = url
        self.id = str(int(datetime.now().timestamp()))  # Unique ID based on timestamp
        self.output_dir = os.path.join(os.getcwd(), "WEBS")
        self.setup_output_directory()

    def setup_output_directory(self): # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def crawl_site(self):
        try:
            print(f"Crawling URL: {self.url}")
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()

            # Save the content to a raw text file
            raw_file_path = os.path.join(self.output_dir, f"{self.id}.txt")
            with open(raw_file_path, "w", encoding="utf-8") as file:
                file.write(f"{self.id} {self.url}\n{response.text}")

            # Create a zip file containing the raw file
            zip_file_path = os.path.join(self.output_dir, f"{self.id}.zip")
            with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(raw_file_path, os.path.basename(raw_file_path))

            # Delete the raw text file after zipping
            os.remove(raw_file_path)

            return zip_file_path

        except requests.exceptions.RequestException as e:
            print(f"Error crawling URL: {e}")
            return None
