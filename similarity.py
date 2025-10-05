def calculate_similarity(s1, s2):
    """
    Calculate the similarity between two strings using the provided formula.
    
    S = (1/4) * (m/|s1| + m/|s2| + (m-t)/m + l/max(|s1|, |s2|))
    
    Where:
    - m is the count of matching characters
    - t is the number of transpositions
    - l is the length of common prefix (up to 4 characters)
    - |s1| and |s2| are the lengths of the strings
    
    Returns a score between 0 and 1.
    """
    if not s1 or not s2:
        return 0.0
    
    # Convert to lowercase for case-insensitive comparison
    s1, s2 = s1.lower(), s2.lower()
    
    # Find matching characters within a limited distance
    s1_len, s2_len = len(s1), len(s2)
    match_distance = max(s1_len, s2_len) // 2 - 1
    
    # Initialize match counters
    s1_matches = [0] * s1_len
    s2_matches = [0] * s2_len
    
    matches = 0
    for i in range(s1_len):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, s2_len)
        
        for j in range(start, end):
            if s1[i] == s2[j] and s2_matches[j] == 0:
                s1_matches[i] = 1
                s2_matches[j] = 1
                matches += 1
                break
    
    if matches == 0:
        return 0.0
    
    # Count transpositions
    transpositions = 0
    k = 0
    
    for i in range(s1_len):
        if s1_matches[i]:
            while s2_matches[k] == 0:
                k += 1
            if s1[i] != s2[k]:
                transpositions += 1
            k += 1
    
    transpositions = transpositions // 2
    
    # Calculate common prefix length (up to 4 characters)
    common_prefix = 0
    for i in range(min(4, min(s1_len, s2_len))):
        if s1[i] == s2[i]:
            common_prefix += 1
        else:
            break
    
    # Calculate the similarity score using the formula
    m = float(matches)
    t = float(transpositions)
    l = float(common_prefix)
    
    term1 = m / s1_len if s1_len > 0 else 0
    term2 = m / s2_len if s2_len > 0 else 0
    term3 = (m - t) / m if m > 0 else 0
    term4 = l / max(s1_len, s2_len) if max(s1_len, s2_len) > 0 else 0
    
    similarity = (1.0 / 4.0) * (term1 + term2 + term3 + term4)
    
    return similarity

def load_legitimate_domains():
    """Load legitimate domains from a file."""
    try:
        with open('legitimate_domains.txt', 'r') as f:
            return [line.strip() for line in f.readlines()]
    except:
        # Fallback to a basic list
        return ["google", "amazon", "facebook", "apple", "microsoft"]

    
def check_domain_similarity(domain, legitimate_domains=None, threshold=0.7):
    """
    Check if the domain is similar to any legitimate domain.
    Returns True if the similarity is above the threshold.
    """
    if legitimate_domains is None:
        legitimate_domains = load_legitimate_domains()  # Call the function to get the list

    max_similarity = 0.0
    most_similar_domain = None

    for legit_domain in legitimate_domains:
        similarity = calculate_similarity(domain, legit_domain)
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_domain = legit_domain

    is_similar = max_similarity >= threshold
    return is_similar, max_similarity, most_similar_domain
