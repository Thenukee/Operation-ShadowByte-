import requests
from bs4 import BeautifulSoup
import pandas as pd
import signal
import sys
import os
from argparse import ArgumentParser, RawDescriptionHelpFormatter, ArgumentTypeError
from datetime import datetime
import logging

def get_response(url, headers, timeout):
    response = None
    error_context = "General Unknown Error"
    exception_text = None

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        error_context = None
    except requests.exceptions.HTTPError as errh:
        error_context = "HTTP Error"
        exception_text = str(errh)
    except requests.exceptions.ProxyError as errp:
        error_context = "Proxy Error"
        exception_text = str(errp)
    except requests.exceptions.ConnectionError as errc:
        error_context = "Error Connecting"
        exception_text = str(errc)
    except requests.exceptions.Timeout as errt:
        error_context = "Timeout Error"
        exception_text = str(errt)
    except requests.exceptions.RequestException as err:
        error_context = "Unknown Error"
        exception_text = str(err)

    return response, error_context, exception_text

def fetch_articles(url, person_name, timeout, start_year, end_year):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
    }
    response, error_context, exception_text = get_response(url, headers, timeout)

    if error_context:
        logging.error(f"Error fetching URL {url}: {error_context} - {exception_text}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    for article in soup.find_all('article'):
        headline = article.find('h1') or article.find('h2') or article.find('h3')
        if headline:
            headline_text = headline.get_text()
            if person_name.lower() in headline_text.lower():
                article_url = article.find('a')['href']
                if not article_url.startswith('http'):
                    article_url = url + article_url
                date_published = article.find('time')
                date_text = date_published.get('datetime') if date_published else 'Unknown'
                article_date = datetime.strptime(date_text, "%Y-%m-%d") if date_text != 'Unknown' else datetime.min

                if start_year <= article_date.year <= end_year:
                    image_url = None
                    img_tag = article.find('img')
                    if img_tag and img_tag.get('src'):
                        image_url = img_tag.get('src')
                        if not image_url.startswith('http'):
                            image_url = url + image_url

                    articles.append((url, article_url, headline_text, image_url, date_text))

    return articles

def timeout_check(value):
    float_value = float(value)
    if float_value <= 0:
        raise ArgumentTypeError(f"Invalid timeout value: {value}. Timeout must be a positive number.")
    return float_value

def handler(signal_received, frame):
    print("\nProcess interrupted. Exiting gracefully...")
    sys.exit(0)

def main():
    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description="Newspaper Article Scraper"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="Newspaper Scraper v1.0",
        help="Display version information.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        default=False,
        help="Display extra debugging information and metrics.",
    )
    parser.add_argument(
        "--output",
        "-o",
        dest="output",
        help="File to save the output of the results.",
    )
    parser.add_argument(
        "--folderoutput",
        "-fo",
        dest="folderoutput",
        help="If using multiple usernames, the output of the results will be saved to this folder.",
    )
    parser.add_argument(
        "--timeout",
        action="store",
        metavar="TIMEOUT",
        dest="timeout",
        type=timeout_check,
        default=60,
        help="Time (in seconds) to wait for response to requests (Default: 60)",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        dest="csv",
        default=False,
        help="Create Comma-Separated Values (CSV) File.",
    )
    parser.add_argument(
        "--xlsx",
        action="store_true",
        dest="xlsx",
        default=False,
        help="Create the standard file for the modern Microsoft Excel spreadsheet (xlsx).",
    )
    parser.add_argument(
        "--print-found",
        action="store_true",
        dest="print_found",
        default=True,
        help="Output sites where the username was found.",
    )
    parser.add_argument(
        "--print-all",
        action="store_true",
        dest="print_all",
        default=False,
        help="Output sites where the username was not found.",
    )
    parser.add_argument(
        "--start-year",
        type=int,
        required=True,
        help="Starting year for the article date range.",
    )
    parser.add_argument(
        "--end-year",
        type=int,
        required=True,
        help="Ending year for the article date range.",
    )
    parser.add_argument(
        "username",
        nargs="+",
        metavar="USERNAMES",
        action="store",
        help="One or more usernames to check with newspapers.",
    )

    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    # If the user presses CTRL-C, exit gracefully
    signal.signal(signal.SIGINT, handler)

    # Define the newspaper sites and their URLs
    site_data = {
        "Daily Mirror": "https://www.dailymirror.lk",
        "Daily News": "https://www.dailynews.lk",
        "The Sunday Times": "https://www.sundaytimes.lk",
        "The Island": "https://www.island.lk",
        "Sunday Observer": "https://www.sundayobserver.lk",
        "News.lk": "https://www.news.lk",
    }

    # Create DataFrame for results
    results_df = []

    for username in args.username:
        print(f"Searching for username: {username}")
        for newspaper, base_url in site_data.items():
            print(f"Searching in {newspaper}...")
            articles = fetch_articles(base_url, username, args.timeout, args.start_year, args.end_year)
            if not articles:
                if args.print_all:
                    results_df.append([newspaper, 'Not Found', 'Not Found', 'Not Found', 'Not Found'])
            else:
                for article in articles:
                    results_df.append([newspaper, article[1], article[2], article[3], article[4]])

    # Save to file or print
    df = pd.DataFrame(results_df, columns=["Newspaper", "Article URL", "Headline", "Image URL", "Publication Date"])
    if args.output:
        df.to_excel(args.output, index=False)
        print(f"Scraping completed. Results saved to {args.output}")
    elif args.folderoutput:
        os.makedirs(args.folderoutput, exist_ok=True)
        for username in args.username:
            result_file = os.path.join(args.folderoutput, f"{username}.xlsx")
            df.to_excel(result_file, index=False)
            print(f"Scraping completed. Results saved to {result_file}")
    elif args.xlsx:
        output_file = "results.xlsx"
        df.to_excel(output_file, index=False)
        print(f"Scraping completed. Results saved to {output_file}")
    else:
        print(df)

    print("\nScraping finished.")

if __name__ == "__main__":
    main()
