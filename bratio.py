# get_bRatio.py

import pandas as pd

# Load the precomputed benign character ratios from the CSV file
bRatio = pd.read_csv('bRatio.csv', index_col=0).squeeze()  # Convert to pandas Series

def get_bRatio(url):
    
    valid_characters = bRatio.index.tolist()  # Get list of valid characters from bRatio
    url = url.replace('.', '')  # Remove periods
    bSum = 0
    bLength = 0

    # Iterate through each character in the URL and calculate the benign ratio
    for char in url:
        if char in valid_characters:
            bSum += bRatio.get(char, 0)
            bLength += 1

    # Return the average benign character ratio
    return bSum / bLength if bLength > 0 else 0
