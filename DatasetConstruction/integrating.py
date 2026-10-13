from flask import Flask, request, jsonify
from AutomatedCrawler import AutomatedCrawler
from main import process_latest_zip
import os

app = Flask(__name__)

@app.route('/crawl', methods=['POST'])
def crawl_site():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    crawler = AutomatedCrawler(url)
    zip_file = crawler.crawl_site()
    if zip_file:
        return jsonify({'message': 'Crawling successful', 'zip_file': zip_file}), 200
    else:
        return jsonify({'error': 'Crawling failed'}), 500

@app.route('/analyze', methods=['POST'])
def analyze_site():
    webs_folder = os.path.join(os.getcwd(), "WEBS")
    if process_latest_zip(webs_folder):
        return jsonify({'message': 'Analysis successful'}), 200
    else:
        return jsonify({'error': 'Analysis failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)
