import math
from collections import Counter

def calculate_entropy(url):
    # Using Counter to count character frequencies
    char_count = Counter(url)
    total_length = len(url)
    
    # Calculate Shannon entropy
    entropy = -sum((count / total_length) * math.log2(count / total_length) for count in char_count.values())
    return entropy

if __name__ == "__main__":
    url = input("Enter the URL for Shannon Entropy calculation: ")
    result = calculate_entropy(url)
    print(f"Shannon Entropy: {result}")
