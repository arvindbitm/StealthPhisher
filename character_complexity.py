from collections import Counter

def calculate_overall_ratio(url):
    """
    Processes a given URL and calculates the overall ratio by summing character ratios
    and dividing by the total number of characters.

    Parameters:
        url (str): The URL to process.

    Returns:
        float: The overall ratio of character frequencies.
        str: Error message if processing fails.
    """
    try:
        # Remove whitespace characters from the URL
        url = url.strip()

        # Remove 'http://' or 'https://' if present
        url = url.replace('http://', '').replace('https://', '')

        # Filter out non-ASCII characters
        url = ''.join(filter(lambda x: x.isascii(), url))

        # Count the frequency of each character
        counter = Counter(url)

        # Calculate the total number of characters
        total_chars = sum(counter.values())

        if total_chars == 0:
            return "URL contains no valid ASCII characters."

        # Calculate the ratio of each character
        char_ratios = {char: count / total_chars for char, count in counter.items()}

        # Calculate the sum of all ratios divided by the total number of characters
        overall_ratio = sum(char_ratios.values()) / total_chars

        return overall_ratio
    except Exception as e:
        return f"Failed to process URL: {e}"
