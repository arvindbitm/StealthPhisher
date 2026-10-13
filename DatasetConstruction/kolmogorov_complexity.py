import zlib

def kolmogorov_complexity(url):
    compressed = zlib.compress(url.encode('utf-8'))
    return len(compressed) / len(url)

# if __name__ == "__main__":
#     url = input("Enter the URL for Kolmogorov Complexity calculation: ")
#     result = kolmogorov_complexity(url)
#     print(f"Kolmogorov Complexity: {result}")
