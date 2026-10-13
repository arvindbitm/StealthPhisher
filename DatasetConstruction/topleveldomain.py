def check_top_level_domain(url):
    with open("domainlist.txt", "r", encoding="ISO-8859-1") as f:
        top_level_domains = [line.strip() for line in f.readlines()]
        domain = url.split('.')[-1]
        if domain in top_level_domains:
            return True, domain
        else:
            return False, "Unknown top-level domain"


url = input("Enter a URL: ")
url = url.replace('https://', '')
is_valid, domain = check_top_level_domain(url)
if is_valid:
    print(f"{url} has a valid top-level domain: {domain}")
else:
    print(f"{url} has an unknown top-level domain: {domain}")
