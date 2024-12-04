# dorking.py
import os
import json
import re
import requests
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from urllib.parse import quote, urlparse
from PIL import Image
from io import BytesIO

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
            raise KeyError(f"Configuration key '{key}' is missing or empty.")
    
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

def create_suspect_folder(suspect_id, base_dir='suspects'):
    """
    Create a dedicated folder for the suspect with necessary subdirectories.
    """
    sanitized_name = sanitize_filename(suspect_id)
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
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Cache file '{cache_file}' contains invalid JSON. Ignoring cache.")
        except Exception as e:
            print(f"Error loading cache: {e}")
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
            seen.add(variant)
            unique_variants.append(variant)
    
    return unique_variants

def perform_google_search(query, num_results=50, search_type=None, retries=3, backoff_factor=2):
    """
    Perform a search using Google Custom Search API with retry logic.
    Supports fetching more results by handling pagination.
    """
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    all_items = []
    start = 1
    while len(all_items) < num_results:
        params = {
            'q': query,
            'cx': GOOGLE_SEARCH_ENGINE_ID,
            'num': min(10, num_results - len(all_items)),
            'start': start
        }
        if search_type == 'image':
            params['searchType'] = 'image'
        
        try:
            response = service.cse().list(**params).execute()
            items = response.get('items', [])
            all_items.extend(items)
            if 'nextPage' in response.get('queries', {}):
                start = response['queries']['nextPage'][0]['startIndex']
            else:
                break
        except HttpError as e:
            if e.resp.status in [500, 502, 503, 504]:
                if retries > 0:
                    time.sleep(backoff_factor)
                    retries -= 1
                    continue
            print(f"Google API Error: {e}")
            break
        except Exception as e:
            print(f"Google API Error: {e}")
            break
    return all_items

def perform_bing_search(query, count=50, offset=0):
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
            print("Bing API rate limit exceeded.")
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
    for idx, item in enumerate(search_results):
        domain = urlparse(item.get('link', '')).netloc
        details.append({
            'id': f'google-web-{idx}',
            'title': item.get('title'),
            'link': item.get('link'),
            'snippet': item.get('snippet'),
            'category': 'google_web_pages',
            'domain': domain
        })
    return details

def extract_google_image_details(search_results):
    """
    Extract details from Google Image search results.
    """
    details = []
    for idx, item in enumerate(search_results):
        domain = urlparse(item.get('link', '')).netloc
        image_url = item.get('image', {}).get('thumbnailLink', '')
        if not image_url:
            continue  # Skip items without an image URL
        details.append({
            'id': f'google-image-{idx}',
            'title': item.get('title'),
            'link': item.get('link'),
            'snippet': item.get('snippet'),
            'category': 'google_images',
            'domain': domain,
            'image_url': image_url
        })
    return details

def extract_google_document_details(search_results):
    """
    Extract details from Google Document search results.
    """
    details = []
    for idx, item in enumerate(search_results):
        domain = urlparse(item.get('link', '')).netloc
        details.append({
            'id': f'google-document-{idx}',
            'title': item.get('title'),
            'link': item.get('link'),
            'snippet': item.get('snippet'),
            'category': 'google_documents',
            'domain': domain
        })
    return details

def extract_bing_web_details(search_results):
    """
    Extract details from Bing Web search results.
    """
    details = []
    for idx, item in enumerate(search_results.get('webPages', {}).get('value', [])):
        domain = urlparse(item.get('url', '')).netloc
        details.append({
            'id': f'bing-web-{idx}',
            'title': item.get('name'),
            'link': item.get('url'),
            'snippet': item.get('snippet'),
            'category': 'bing_web_pages',
            'domain': domain
        })
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
            image = Image.open(BytesIO(response.content))
            image.save(save_path)
            print(f"Image saved to {save_path}")
        else:
            print(f"Failed to download image from {url}. Status code: {response.status_code}")
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
            print(f"Failed to download document from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Exception occurred while downloading document from {url}: {e}")

def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file.
    """
    try:
        import PyPDF2
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error extracting text from PDF {file_path}: {e}")
        return ""

def process_results(category, items, suspect_folder):
    """
    Process and handle results based on their category.
    """
    print(f"\n=== {category.replace('_', ' ').title()} ===")
    if not items:
        print("No items found.")
        return
    for idx, item in enumerate(items, start=1):
        print(f"{idx}. {item['title']} - {item['link']}")
        # Save details based on category
        if category in ['google_web_pages', 'bing_web_pages']:
            # Save web page details
            pass  # Implement as needed
        elif category == 'google_images':
            # Download and save image
            image_path = os.path.join(suspect_folder, 'images', f"image_{idx}.jpg")
            download_image(item['image_url'], image_path)
        elif category == 'google_documents':
            # Download and process document
            doc_path = os.path.join(suspect_folder, 'documents', f"document_{idx}.pdf")
            download_document(item['link'], doc_path)
            text = extract_text_from_pdf(doc_path)
            # Save extracted text if needed
            text_path = os.path.join(suspect_folder, 'documents', f"document_{idx}.txt")
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(text)

def build_cache_key(engine, category, query):
    """
    Build a unique cache key based on search engine, category, and query.
    """
    return f"{engine}_{category}_{query}"

def perform_searches(selected_variants, search_types, suspect_folder, cache, all_details, total_results=50):
    """
    Perform searches for each selected name variant and search type.
    """
    for variant in selected_variants:
        for search_type in search_types:
            cache_key = build_cache_key(search_type, variant, search_type)
            if cache_key in cache:
                print(f"Using cached results for {cache_key}")
                all_details[search_type].extend(cache[cache_key])
                continue
            if search_type == 'google_web_pages':
                results = perform_google_search(variant, num_results=total_results, search_type=None)
                details = extract_google_web_details(results)
            elif search_type == 'google_images':
                results = perform_google_search(variant, num_results=total_results, search_type='image')
                details = extract_google_image_details(results)
            elif search_type == 'google_documents':
                results = perform_google_search(variant, num_results=total_results, search_type=None)
                details = extract_google_document_details(results)
            elif search_type == 'bing_web_pages':
                results = perform_bing_search(variant, count=total_results)
                details = extract_bing_web_details(results)
            else:
                details = []
            all_details[search_type].extend(details)
            cache[cache_key] = details
            save_cache(suspect_folder, cache)

def perform_dorking(suspect_id, search_all=True, search_engines=['google', 'bing']):
    """
    Perform dorking for a suspect with specified options.
    """
    # Load suspect details
    suspect_folder = create_suspect_folder(suspect_id)
    details_file = os.path.join(suspect_folder, 'details.json')
    with open(details_file, 'r', encoding='utf-8') as f:
        suspect_details = json.load(f)
    suspect_name = suspect_details['name']

    # Generate name variants
    name_variants = generate_name_variants(suspect_name) if search_all else [suspect_name]

    # Define search types based on selected search engines
    search_types = []
    for engine in search_engines:
        if engine.lower() == 'google':
            search_types.extend(['google_web_pages', 'google_images', 'google_documents'])
        elif engine.lower() == 'bing':
            search_types.append('bing_web_pages')

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
        all_details=all_details,
        total_results=50
    )

    # Process and save all collected results
    for category, items in all_details.items():
        process_results(category, items, suspect_folder)

    # Save all results to a JSON file within the suspect's folder
    results_file = os.path.join(suspect_folder, 'results.json')
    save_to_json(all_details, filename=results_file)

    print(f"Dorking completed for suspect ID {suspect_id}.")

# ------------------------------ Instagram Scraping ------------------------------

def perform_instagram_scraping(suspect_name, num_results=20):
    """
    Perform Google Dorking to scrape Instagram usernames and links based on the suspect's name.
    """
    query = f'"{suspect_name}" site:instagram.com'
    try:
        service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
        res = service.cse().list(q=query, cx=GOOGLE_SEARCH_ENGINE_ID, num=10).execute()
        results = res.get('items', [])
        
        instagram_data = []
        for item in results[:num_results]:
            link = item.get('link')
            username = extract_instagram_username(link)
            if username:
                instagram_data.append({
                    'username': username,
                    'link': link
                })
        return instagram_data
    except HttpError as e:
        print(f"An error occurred: {e}")
        return []

def extract_instagram_username(url):
    """
    Extract Instagram username from the URL.
    """
    parsed_url = urlparse(url)
    path = parsed_url.path.strip('/')
    if path:
        return path.split('/')[0]
    return None