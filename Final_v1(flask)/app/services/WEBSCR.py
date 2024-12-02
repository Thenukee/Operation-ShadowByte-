import requests
from bs4 import BeautifulSoup
import time
import urllib.parse

def fetch_page_content(url, headers):
    """Fetches page content from the given URL."""
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def clean_date(date_text):
    """Cleans the date text by removing any extra text like '1 min read'."""
    # Split the date text by spaces and take the part that looks like a date
    date_parts = date_text.split()
    for i in range(len(date_parts)):
        if date_parts[i].isdigit() and len(date_parts[i]) == 4:  # Likely the year
            return ' '.join(date_parts[i-2:i+1])  # Return the date including day, month, and year
    return date_text  # Return the original text if no specific pattern is found

def extract_news_items(soup, site_config):
    """Extracts news items from the page soup based on site configuration."""
    articles = soup.select(site_config['article_selector'])
    news_items = []
    
    for article in articles:
        headline = article.get_text().strip()
        url = article.find('a')['href'] if article.find('a') else 'No URL found'
        url = urllib.parse.urljoin(site_config['base_url'], url)
        
        date_element = article.select_one(site_config['date_selector'])
        date = clean_date(date_element.get_text().strip()) if date_element else 'No date found'
        
        news_items.append({
            'headline': headline,
            'date': date,
            'url': url
        })
        
    return news_items

def search_website(site_name, site_config, person_name):
    """Searches for a person's name on a given website."""
    query = urllib.parse.quote_plus(person_name)
    search_url = site_config['search_url'].format(query)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    
    print(f"\nSearching {site_name} for '{person_name}'...\n")

    page_content = fetch_page_content(search_url, headers)
    
    if page_content:
        soup = BeautifulSoup(page_content, 'html.parser')
        news_items = extract_news_items(soup, site_config)
        
        if news_items:
            for item in news_items:
                print(f"{'='*50}")
                print(f"Headline    : {item['headline']}")
                print(f"Date        : {item['date']}")
                print(f"URL         : {item['url']}")
                print(f"{'='*50}")
                time.sleep(1)
        else:
            print(f"No results found on {site_name}.")
    else:
        print(f"Failed to retrieve the page from {site_name}.")

# Configuration for different news sites
news_sites = {
    'Ada Derana': {
        'base_url': 'https://www.adaderana.lk',
        'search_url': 'https://www.adaderana.lk/search_results.php?mode=2&show=1&query={}',
        'article_selector': 'div.news-story',
        'date_selector': 'body > div.container.main-content > div > div.col-xs-12.col-sm-8.col-lg-7 > div:nth-child(3) > div > div.comments.pull-right.hidden-xs > a:nth-child(2)'
    },
    'News Cutter': {
        'base_url': 'https://www.newscutter.lk',
        'search_url': 'https://www.newscutter.lk/?post_types=&s={}',
        'article_selector': 'div.post_content.entry-content',
        'date_selector': '#post-66703 > div.post_content.entry-content > div.post_meta > span > a'
    },
    'Sunday Observer': {
        'base_url': 'https://www.sundayobserver.lk',
        'search_url': 'https://www.sundayobserver.lk/?s={}',
        'article_selector': 'div.content-list-right',
        'date_selector': '#post-27009 > div.content-list-right.content-list-center > div.header-list-style > div.grid-post-box-meta > span.otherl-date > time'
    },
    'Onlanka': {
        'base_url': 'https://www.onlanka.com',
        'search_url': 'https://www.onlanka.com/?s={}',
        'article_selector': 'div.post-contents',
        'date_selector': '#post-70660 > div.post-contents > div.post-category > span'
    },
    'Lanka Truth': {
        'base_url': 'https://lankatruth.com/en',
        'search_url': 'https://lankatruth.com/en/?s={}',
        'article_selector': 'article.elementor-post',
        'date_selector': 'body > div > div.site-inner > div > div > section > div > div > div > div > div > div > article.elementor-post.elementor-grid-item.post-25972.post.type-post.status-publish.format-standard.has-post-thumbnail.category-economy.category-smartphones.category-political.entry > div > div.elementor-post__meta-data > span.elementor-post-date'
    },
    'Island': {
        'base_url': 'https://island.lk',
        'search_url': 'https://island.lk/?s={}',
        'article_selector': 'article',
        'date_selector': 'body > div.container.main-content > div > div.col-xs-12.col-sm-8.col-lg-7 > div:nth-child(3) > div > div.comments.pull-right.hidden-xs > a:nth-child(2)'
    },
    'News.lk': {
        'base_url': 'https://www.news.lk',
        'search_url': 'https://www.news.lk/component/search/?searchword={}&ordering=newest&searchphrase=all&limit=20',
        'article_selector': 'dl.search-results',
        'date_selector': '#sp-component > div > div.search > dl > dd:nth-child(4)'
    },
    'Lanka News Web': {
        'base_url': 'https://lankanewsweb.net',
        'search_url': 'https://lankanewsweb.net/?s={}',
        'article_selector': 'article',
        'date_selector': '#tdi_85 > div > div.vc_column.tdi_88.wpb_column.vc_column_container.tdc-column.td-pb-span8 > div > div.vc_row_inner.tdi_90.vc_row.vc_inner.wpb_row.td-pb-row > div.vc_column_inner.tdi_95.wpb_column.vc_column_container.tdc-inner-column.td-pb-span9 > div > div > div.td_block_wrap.tdb_single_date.tdi_97.td-pb-border-top.td_block_template_1.tdb-post-meta > div.tdb-block-inner.td-fix-index > time'
    },
    'Economy Next': {
        'base_url': 'https://economynext.com',
        'search_url': 'https://economynext.com/?s={}',
        'article_selector': 'div.story-grid',
        'date_selector': 'body > div.middle-level-stories > div.story-grid > div:nth-child(2) > div.story-grid-text > div.author-story-grid-time-padding.author-story-grid-mobile-sup > div.read-time-comment > div > span.article-publish-date'
    }
}

# Input person's name
person_name = input("Enter the person's name to search for: ")

# Search on all websites
for site_name, site_config in news_sites.items():
    search_website(site_name, site_config,person_name)
    