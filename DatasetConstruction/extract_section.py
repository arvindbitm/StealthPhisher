import os
import re
import json

def clean_json_from_text(text):
    # Remove the unwanted '''json{ content }''' wrapper
    cleaned_text = re.sub(r"'''json{(.*)}'''", r'\1', text, flags=re.DOTALL)
    return cleaned_text

def process_raw_response(url):
    domain_name = re.sub(r"https?://", "", url).split('/')[0]
    txt_file_path = f"D:\\GUI\\static\\gen_reports\\{domain_name}.txt"
    json_file_path = f"D:\\GUI\\static\\gen_reports\\{domain_name}.json"

    try:
        if not os.path.exists(txt_file_path):
            raise FileNotFoundError(f"The file {txt_file_path} does not exist.")

        try:
            with open(txt_file_path, "r", encoding="utf-8") as file:
                raw_content = file.read()
        except UnicodeDecodeError:
            with open(txt_file_path, "r", encoding="ISO-8859-1") as file:
                raw_content = file.read()

        # Clean the raw content to remove '''json{ content }'''
        cleaned_content = clean_json_from_text(raw_content)

        # Ensure the output directory exists
        output_dir = os.path.dirname(json_file_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the cleaned content directly into the JSON file
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            # Saving the cleaned content as a JSON file, wrapped in a simple structure
            json.dump({"content": cleaned_content}, json_file, indent=4)

        print(f"Cleaned content successfully saved at {json_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# url = "http://google.com"
# process_raw_response(url)
