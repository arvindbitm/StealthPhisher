# get_mRatio.py

import pandas as pd

# Load the precomputed phishing character ratios from the CSV file
mRatio = pd.read_csv('mRatio.csv', index_col=0).squeeze()  # Convert to pandas Series

def get_mRatio(url):
    """
    Given a URL, compute the phishing character ratio based on precomputed mRatio values.
    
    Parameters:
    url (str): The URL to analyze
    
    Returns:
    float: The phishing character ratio for the URL
    """
    valid_characters = mRatio.index.tolist()  # Get list of valid characters from mRatio
    url = url.replace('.', '')  # Remove periods
    mSum = 0
    mLength = 0

    # Iterate through each character in the URL and calculate the phishing ratio
    for char in url:
        if char in valid_characters:
            mSum += mRatio.get(char, 0)
            mLength += 1

    # Return the average phishing character ratio
    return mSum / mLength if mLength > 0 else 0
