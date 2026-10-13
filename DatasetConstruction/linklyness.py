import numpy as np
import pandas as pd
import os

# Function to extract and normalize the domain from a URL
def extract_domain(url: str) -> str:
    try:
        if url.startswith("http://") or url.startswith("https://"):
            url = url[url.index("//") + 2:]
        if url.startswith("www."):
            url = url[4:]
        slash_index = url.find('/')
        domain = url[:slash_index] if slash_index != -1 else url
        return domain.lower().strip()  # Normalize to lowercase and strip whitespace
    except Exception as e:
        print(f"Error extracting domain from URL '{url}': {e}")
        return "INVALID"

# CPU Likeliness Index Calculation (replaced CuPy with NumPy)
def likeliness_index_cpu(s1: str, s2: str) -> float:
    try:
        # Convert strings to arrays of ord values
        arr1 = np.array([ord(c) for c in s1], dtype=np.int32)
        arr2 = np.array([ord(c) for c in s2], dtype=np.int32)

        len1, len2 = len(arr1), len(arr2)
        match_distance = max(len1, len2) // 2 - 1

        # Matching characters
        matches1 = np.zeros(len1, dtype=bool)
        matches2 = np.zeros(len2, dtype=bool)

        for i in range(len1):
            start = max(0, i - match_distance)
            end = min(len2, i + match_distance + 1)
            for j in range(start, end):
                if not matches2[j] and arr1[i] == arr2[j]:
                    matches1[i] = True
                    matches2[j] = True
                    break

        m = np.sum(matches1)
        if m == 0:
            return 0.0

        # Transpositions
        t = np.sum(arr1[matches1] != arr2[matches2]) // 2

        # Common prefix length
        prefix_length = 0
        for i in range(min(4, len1, len2)):
            if arr1[i] == arr2[i]:
                prefix_length += 1
            else:
                break

        # Calculate the Likeliness Index
        return float((1 / 4) * ((m / len1) + (m / len2) + ((m - t) / m) + (prefix_length / max(len1, len2))))
    except Exception as e:
        print(f"Error calculating Likeliness Index: {e}")
        return 0.0

# Function to search for a target URL in the dataset and calculate its score
def calculate_likelynessindex(target_url: str, chunk_size: int = 1000):
    input_csv = "top10milliondomains.csv"  # Default input CSV file
    try:
        df = pd.read_csv(input_csv, chunksize=chunk_size)
        target_domain = extract_domain(target_url)

        for chunk in df:
            if 'url' not in chunk.columns:
                raise ValueError("The input CSV must contain a column named 'url'.")

            chunk['domain'] = chunk['url'].apply(extract_domain)

            # Calculate scores for each domain in the chunk
            scores = chunk['domain'].apply(lambda x: likeliness_index_cpu(target_domain, x))
            if (scores > 0).any():
                max_score = scores.max()
                return max_score

        return 0.0
    except Exception as e:
        print(f"Error searching the dataset: {e}")
        return 0.0

# Example usage:
# target_urls = [
#     "http://117.206.70.128:38639/bin.sh",
#     "https://instagram.com",
#     "https://multigrad.in",
#     "https://clarobrasilia.com.br/tv-por-assinatura/",
#     "http://blue3store.talentossolucoes.com.br/"
# ]

# for target_url in target_urls:
#     score = calculate_likelynessindex(target_url)
#     print(f"Likeliness Index for '{target_url}': {score}")
