import os
import json
from offline_analyzer import OfflineCodeAnalyzer

def main():
    input_folder = "WEBS"
    output_folder = "WEBS"
    output_file = os.path.join(output_folder, "features.json")

    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the latest file in the WEBS folder
    files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(".txt")]

    if not files:
        print("No files found in the WEBS folder.")
        return

    latest_file = max(files, key=os.path.getctime)
    print(f"Processing file: {latest_file}")

    # Read the crawled web content
    with open(latest_file, "rb") as f:
        web_content = f.read()

    # Debug: Check the length of the content to ensure it's valid
    print("Web Content Length:", len(web_content))
    if len(web_content) == 0:
        print("Web content is empty.")
        return

    # Extract URL from the HTML file (First line contains the URL and ID)
    with open(latest_file, "r",encoding="utf-8") as f:
        first_line = f.readline().strip()
        if " " not in first_line:
            print("Error: Invalid file format.")
            return

        file_id, url_from_file = first_line.split(" ", 1)

    # Check if the URL matches the provided URL
    url_to_analyze = url_from_file  # The URL you want to analyze, adjust as needed
    if url_from_file != url_to_analyze:
        print(f"URL mismatch. File URL: {url_from_file}, Provided URL: {url_to_analyze}")
        return False

    # Analyze the content to extract features
    try:
        features = OfflineCodeAnalyzer(web_content)

        # Debug: Check if features are being returned
        print("Extracted Features:", features)

        if not features:
            print("No features found, nothing to save.")
            return

        # Save features to a JSON file in the WEBS folder
        with open(output_file, "w") as f:
            json.dump(features, f, indent=4)

        print(f"Features saved to: {output_file}")

    except Exception as e:
        print(f"Error during feature extraction: {e}")
        return

if __name__ == "__main__":
    main()
