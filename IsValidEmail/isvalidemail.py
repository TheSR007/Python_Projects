import re
import requests

def main():
    while True:
        print("Is Valid Email? ", isValidEmail(input("What's your email?").strip().lower()))



'''
regular expression that modern browser uses 
change to your needs
'''
regex = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$" 

def isValidEmail(email):
    if re.fullmatch(regex, email):
        domain = re.search(r"\.([a-zA-Z0-9-]+)$", email)
        if domain.group(1) in get_domains():
            return True
    return False


def get_domains():
    domains = []
    try:
        with open("domains.txt", "r") as file:
            for domain in file:
                domains.append(domain.strip().lower())
        return domains
    except FileNotFoundError:
        response = requests.get('https://data.iana.org/TLD/tlds-alpha-by-domain.txt')
        top_domains = response.text.splitlines()

        with open("domains.txt", "w") as file:
            for domain in top_domains:
                file.write(f"{domain}\n")
                domains.append(domain.strip().lower())
        return domains


if __name__ == "__main__":
    main()