def fractal_dimension(url_path):
    tokens = url_path.split('/')
    unique_tokens = set(tokens)
    return len(unique_tokens) / len(tokens) if tokens else 0

# if __name__ == "__main__":
#     url = input("Enter the URL for Fractal Dimension calculation: ")
#     result = fractal_dimension(url)
#     print(f"Fractal Dimension: {result}")
