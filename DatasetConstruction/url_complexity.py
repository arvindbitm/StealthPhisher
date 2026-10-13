import re
import urllib.parse

def calculate_url_complexity(url):
    # Parse the URL
    parsed_url = urllib.parse.urlparse(url)
    
    # Calculate the length of the URL
    length_score = min(len(url) / 2, 100)  # Normalize to 0-100
    
    # Count the number of query parameters
    query_params = urllib.parse.parse_qs(parsed_url.query)
    num_params = len(query_params)
    param_score = min(num_params * 10, 100)  # Assuming 10 params can be very complex
    
    # Count the number of special characters
    special_chars = re.findall(r'[^\w\s]', url)  # Find all non-alphanumeric and non-space characters
    special_char_score = min(len(special_chars) * 2, 100)  # Each special char adds complexity
    
    # Calculate the path depth
    path_depth = parsed_url.path.count('/')
    path_depth_score = min(path_depth * 10, 100)  # Each level of depth adds complexity
    
    # Calculate the total score
    total_score = (length_score * 0.25 + param_score * 0.25 + special_char_score * 0.25 + path_depth_score * 0.25)
    total_score = min(total_score, 100)  # Ensure the score is between 0 and 100
    
    return total_score

def main():
    url = input("Enter a URL to check its complexity: ")
    score = calculate_url_complexity(url)
    print(f"URL: {url}\nComplexity Score: {score:.2f}/100\n")

if __name__ == "__main__":
    main()
