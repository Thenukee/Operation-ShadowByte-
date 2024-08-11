import requests
import argparse

API_KEY = 'your_api_key_here'
HEADERS = {
    'hibp-api-key': API_KEY,
    'User-Agent': 'Python script to check email breaches'
}

def check_email(email):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 404:
        print(f"[i] {email} has not been breached.")
    elif response.status_code == 200:
        print(f"[!] {email} has been breached!")
        breaches = response.json()
        for breach in breaches:
            print(f"  - {breach['Name']}: {breach['Description']}")
    else:
        print(f"[?] Error checking {email}: {response.status_code}")

def main():
    parser = argparse.ArgumentParser(description='Check emails against Have I Been Pwned API.')
    parser.add_argument('-e', '--email', type=str, help='Single email address to check')
    parser.add_argument('-f', '--file', type=str, help='File with email addresses to check (one per line)')
    args = parser.parse_args()

    if args.email:
        check_email(args.email)
    elif args.file:
        with open(args.file, 'r') as file:
            emails = file.readlines()
            for email in emails:
                check_email(email.strip())
    else:
        email = input("Enter the email address to check: ")
        check_email(email)

if __name__ == "__main__":
    main()