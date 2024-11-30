import os
import json
import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from urllib.parse import quote
from PIL import Image
from io import BytesIO
import PyPDF2
import time
import re
import uuid

# ------------------------------ Configuration ------------------------------

def load_config(config_file='config.json'):
    """
    Load API credentials from a JSON configuration file.
    """
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    required_keys = ['GOOGLE_API_KEY', 'GOOGLE_SEARCH_ENGINE_ID', 'BING_API_KEY']
    for key in required_keys:
        if key not in config or not config[key]:
            raise KeyError(f"'{key}' is missing or empty in the configuration file.")
    
    return config

# Load configuration
config = load_config()

GOOGLE_API_KEY = config['GOOGLE_API_KEY']
GOOGLE_SEARCH_ENGINE_ID = config['GOOGLE_SEARCH_ENGINE_ID']
BING_API_KEY = config['BING_API_KEY']
BING_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"

# ------------------------------ Helper Functions ------------------------------

def sanitize_filename(name):
    """
    Sanitize the suspect's name to create a safe folder name.
    """
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', name)
    return sanitized

def create_suspect_folder(suspect_name, base_dir='suspects'):
    """
    Create a dedicated folder for the suspect with necessary subdirectories.
    """
    sanitized_name = sanitize_filename(suspect_name)
    suspect_folder = os.path.join(base_dir, sanitized_name)
    images_folder = os.path.join(suspect_folder, 'images')
    documents_folder = os.path.join(suspect_folder, 'documents')
    os.makedirs(images_folder, exist_ok=True)
    os.makedirs(documents_folder, exist_ok=True)
    return suspect_folder

def load_cache(suspect_folder):
    """
    Load the cache from the suspect's cache.json file.
    """
    cache_file = os.path.join(suspect_folder, 'cache.json')
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            return cache
        except json.JSONDecodeError:
            print(f"Error: Cache file '{cache_file}' contains invalid JSON.")
            return {}
        except Exception as e:
            print(f"Error: An error occurred while reading cache file '{cache_file}': {e}")
            return {}
    else:
        return {}

def save_cache(suspect_folder, cache):
    """
    Save the cache to the suspect's cache.json file.
    """
    cache_file = os.path.join(suspect_folder, 'cache.json')
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Failed to save cache to JSON: {e}")

def generate_name_variants(full_name):
    """
    Generate name variants based on the full name provided without dots.
    """
    name_parts = full_name.split()
    if len(name_parts) < 2:
        raise ValueError("Please enter at least first and last name.")
    
    first_name = name_parts[0]
    last_name = name_parts[-1]
    middle_names = name_parts[1:-1]
    
    variants = []
    
    # Full name
    variants.append(full_name)
    
    # First name + last name
    variants.append(f"{first_name} {last_name}")
    
    # First initial + last name
    first_initial = first_name[0]
    variants.append(f"{first_initial} {last_name}")
    
    # If middle names exist
    if middle_names:
        middle_initials = ''.join([name[0] for name in middle_names])
        # First initial + middle initials + last name
        variants.append(f"{first_initial} {middle_initials} {last_name}")
        # First name + middle initial + last name
        middle_initial = middle_names[0][0]
        variants.append(f"{first_name} {middle_initial} {last_name}")
        # First initial + middle name(s) + last name
        variants.append(f"{first_initial} {' '.join(middle_names)} {last_name}")
        # First name + middle name(s) + last initial
        middle_name = ' '.join(middle_names)
        last_initial = last_name[0]
        variants.append(f"{first_name} {middle_name} {last_initial}")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_variants = []
    for variant in variants:
        if variant not in seen:
            unique_variants.append(variant)
            seen.add(variant)
    
    return unique_variants

def perform_google_search(query, num_results=10, start=1, search_type=None, retries=3, backoff_factor=2):
    """
    Perform a search using Google Custom Search API with retry logic.
    """
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    params = {
        'q': query,
        'cx': GOOGLE_SEARCH_ENGINE_ID,
        'num': num_results,
        'start': start
    }
    if search_type == 'image':
        params['searchType'] = 'image'
    
    for attempt in range(1, retries + 1):
        try:
            res = service.cse().list(**params).execute()
            return res
        except HttpError as e:
            if e.resp.status == 429:
                print("Error: Google Custom Search API quota exceeded for the day.")
                return {}
            elif e.resp.status in [500, 502, 503, 504]:
                wait_time = backoff_factor ** attempt
                print(f"Google API server error (status {e.resp.status}). Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"An HTTP error occurred with Google API: {e}")
                return {}
        except Exception as e:
            print(f"An unexpected error occurred with Google API: {e}")
            return {}
    print("Max retries exceeded for Google API. Moving to the next search option.")
    return {}

def perform_bing_search(query, count=10, offset=0):
    """
    Perform a Bing Web Search.
    """
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    params = {
        "q": query,
        "count": count,
        "offset": offset,
        "mkt": "en-US",
        "safesearch": "Moderate"
    }

    try:
        response = requests.get(BING_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        if response.status_code == 429:
            print("Error: Bing Search API rate limit exceeded.")
        else:
            print(f"Bing HTTP Error: {errh}")
        return {}
    except requests.exceptions.RequestException as e:
        print(f"Bing Request Exception: {e}")
        return {}
    except Exception as e:
        print(f"Bing Unexpected Error: {e}")
        return {}

def extract_google_web_details(search_results):
    """
    Extract details from Google Web search results.
    """
    details = []
    if 'items' in search_results:
        for item in search_results['items']:
            detail = {
                'title': item.get('title'),
                'link': item.get('link'),
                'snippet': item.get('snippet')
            }
            details.append(detail)
    return details

def extract_google_image_details(search_results):
    """
    Extract details from Google Image search results.
    """
    details = []
    if 'items' in search_results:
        for item in search_results['items']:
            detail = {
                'title': item.get('title'),
                'link': item.get('link'),
                'image_thumbnail': item.get('image', {}).get('thumbnailLink'),
                'image_context': item.get('image', {}).get('contextLink')
            }
            details.append(detail)
    return details

def extract_bing_web_details(search_results):
    """
    Extract details from Bing Web search results.
    """
    details = []
    if 'webPages' in search_results and 'value' in search_results['webPages']:
        for item in search_results['webPages']['value']:
            detail = {
                'title': item.get('name'),
                'link': item.get('url'),
                'snippet': item.get('snippet')
            }
            details.append(detail)
    return details

def save_to_json(data, filename='results.json'):
    """
    Save the collected data to a JSON file.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"\nAll results have been saved to {filename}")
    except Exception as e:
        print(f"Failed to save results to JSON: {e}")

def download_image(url, save_path):
    """
    Download an image from a URL.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img_format = img.format.lower()
            if img_format not in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                img_format = 'jpg'  # Default format
            save_path = f"{save_path}.{img_format}"
            img.save(save_path)
            print(f"Image saved to {save_path}")
        else:
            print(f"Failed to download image from {url}: Status Code {response.status_code}")
    except Exception as e:
        print(f"Exception occurred while downloading image from {url}: {e}")

def download_document(url, save_path):
    """
    Download a document from a URL.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"Document saved to {save_path}")
        else:
            print(f"Failed to download document from {url}: Status Code {response.status_code}")
    except Exception as e:
        print(f"Exception occurred while downloading document from {url}: {e}")

def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file.
    """
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        return text
    except Exception as e:
        print(f"Failed to extract text from {file_path}: {e}")
        return ""

def process_results(category, items, suspect_folder):
    """
    Process and handle results based on their category.
    """
    print(f"\n=== {category.replace('_', ' ').title()} ===")
    if not items:
        print("No results found.")
        return
    for idx, item in enumerate(items, start=1):
        print(f"\nResult {idx}:")
        for key, value in item.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

        # Optional: Download Images/Documents
        if category.startswith('google_images') or category == 'images':
            img_url = item.get('link')
            if img_url:
                img_save_path = os.path.join(suspect_folder, 'images', f"{category}_result_{idx}")
                download_image(img_url, img_save_path)
        elif category.startswith('google_documents') or category == 'documents':
            doc_url = item.get('link')
            if doc_url:
                doc_save_path = os.path.join(suspect_folder, 'documents', f"{category}_result_{idx}.pdf")
                download_document(doc_url, doc_save_path)
                # Extract text from PDF
                extracted_text = extract_text_from_pdf(doc_save_path)
                if extracted_text:
                    text_save_path = os.path.join(suspect_folder, 'documents', f"{category}_result_{idx}.txt")
                    try:
                        with open(text_save_path, 'w', encoding='utf-8') as f:
                            f.write(extracted_text)
                        print(f"Extracted text saved to {text_save_path}")
                    except Exception as e:
                        print(f"Failed to save extracted text: {e}")

def build_cache_key(engine, category, query):
    """
    Build a unique cache key based on search engine, category, and query.
    """
    return f"{engine}_{category}_{query}"

def perform_searches(selected_variants, search_types, suspect_folder, cache, all_details, total_results=50, results_per_request=10):
    """
    Perform searches for each selected name variant and search type.
    """
    for variant in selected_variants:
        for search_type in search_types:
            engine = search_type['engine']
            category = search_type['type']
            query = search_type['query'].format(name=variant)
            search_engine = 'google' if engine == 'google' else 'bing'

            # Build a unique cache key
            cache_key = build_cache_key(engine, category, query)

            print(f"\nSearching for: {query} using {engine.capitalize()} Search")

            if cache_key in cache:
                # Use cached data
                print(f"Loading cached results for query: {query}")
                search_results = cache[cache_key]
                # Process cached results
                if engine == 'google':
                    if category in ['web_pages', 'documents']:
                        details = extract_google_web_details(search_results)
                        key = f"google_{category}"
                        all_details[key].extend(details)
                    elif category == 'images':
                        details = extract_google_image_details(search_results)
                        key = f"google_{category}"
                        all_details[key].extend(details)
                elif engine == 'bing':
                    if category == 'web_pages':
                        details = extract_bing_web_details(search_results)
                        key = f"bing_{category}"
                        all_details[key].extend(details)
                continue  # Skip to the next search type

            else:
                # No cached data; perform search and cache the results
                if engine == 'google':
                    # Perform paginated Google Search
                    search_results = {}
                    for start in range(1, total_results + 1, results_per_request):
                        temp_results = perform_google_search(
                            query=query,
                            num_results=results_per_request,
                            start=start,
                            search_type=search_type.get('search_type', None)
                        )

                        if not temp_results:
                            print("No more results or an error occurred with Google Search.")
                            break

                        if category in ['web_pages', 'documents']:
                            details = extract_google_web_details(temp_results)
                            key = f"google_{category}"
                            all_details[key].extend(details)
                        elif category == 'images':
                            details = extract_google_image_details(temp_results)
                            key = f"google_{category}"
                            all_details[key].extend(details)

                        print(f"Fetched results {start} to {start + results_per_request - 1} from Google.")
                        # Optional: Delay to respect rate limits
                        time.sleep(1)  # Sleep for 1 second between requests

                    # Update cache with all fetched results
                    cache[cache_key] = temp_results

                elif engine == 'bing':
                    # Perform paginated Bing Search
                    search_results = {}
                    for offset in range(0, total_results, results_per_request):
                        temp_results = perform_bing_search(
                            query=query,
                            count=results_per_request,
                            offset=offset
                        )

                        if not temp_results:
                            print("No more results or an error occurred with Bing Search.")
                            break

                        details = extract_bing_web_details(temp_results)
                        key = f"bing_{category}"
                        all_details[key].extend(details)

                        print(f"Fetched results {offset + 1} to {offset + results_per_request} from Bing.")
                        # Optional: Delay to respect rate limits
                        time.sleep(1)  # Sleep for 1 second between requests

                    # Update cache with all fetched results
                    cache[cache_key] = temp_results

                # Save cache after scraping new data
                save_cache(suspect_folder, cache)

def perform_dorking(suspect_name, search_all=True, search_engines=['google', 'bing']):
    """
    Perform dorking for a suspect with specified options.
    """
    # Generate name variants
    name_variants = generate_name_variants(suspect_name) if search_all else [suspect_name]

    # Define search types based on selected search engines
    search_types = []
    for engine in search_engines:
        if engine.lower() == 'google':
            search_types.extend([
                {'engine': 'google', 'type': 'web_pages', 'query': '"{name}"'},
                {'engine': 'google', 'type': 'documents', 'query': '"{name}" filetype:pdf'},
                {'engine': 'google', 'type': 'images', 'query': '"{name}"', 'search_type': 'image'},
                {'engine': 'google', 'type': 'web_pages', 'query': '"{name}" site:linkedin.com'}
            ])
        elif engine.lower() == 'bing':
            search_types.append({'engine': 'bing', 'type': 'web_pages', 'query': '"{name}"'})

    # Create suspect folder
    suspect_folder = create_suspect_folder(suspect_name)

    # Load cache
    cache = load_cache(suspect_folder)

    # Initialize all_details dictionary
    all_details = {
        'google_web_pages': [],
        'google_images': [],
        'google_documents': [],
        'bing_web_pages': []
    }

    # Perform searches
    perform_searches(
        selected_variants=name_variants,
        search_types=search_types,
        suspect_folder=suspect_folder,
        cache=cache,
        all_details=all_details
    )

    # Process and save all collected results
    for category, items in all_details.items():
        process_results(category, items, suspect_folder)

    # Save all results to a JSON file within the suspect's folder
    results_file = os.path.join(suspect_folder, 'results.json')
    save_to_json(all_details, filename=results_file)

    print(f"Dorking completed for {suspect_name}.")
