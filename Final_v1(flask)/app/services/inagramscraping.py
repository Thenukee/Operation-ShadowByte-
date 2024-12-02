import os
import sys
import time
import json
import random
import logging
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    WebDriverException,
    NoSuchElementException,
    TimeoutException,
)
from selenium_stealth import stealth
from fake_useragent import UserAgent

# Configure Logging
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# Fetch Credentials from Environment Variables
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

if not INSTAGRAM_USERNAME or not INSTAGRAM_PASSWORD:
    logging.error("Instagram credentials not set in environment variables.")
    print("Error: Instagram username and password must be set as environment variables.")
    sys.exit(1)

def prepare_browser(headless=False):
    """
    Initializes and configures the Selenium WebDriver with stealth settings.
    
    Args:
        headless (bool): Whether to run the browser in headless mode.
    
    Returns:
        webdriver.Chrome: Configured Selenium Chrome WebDriver instance.
    """
    chrome_options = webdriver.ChromeOptions()

    if headless:
        chrome_options.add_argument("--headless")
    
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Rotate User-Agent using fake_useragent
    ua = UserAgent()
    try:
        user_agent = ua.random
    except Exception as e:
        logging.warning(f"Failed to fetch random User-Agent: {e}. Using default User-Agent.")
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
                     " Chrome/115.0.0.0 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    # Initialize WebDriver
    try:
        # Ensure ChromeDriver is in PATH or specify the executable path
        service = ChromeService()  # Assumes chromedriver is in PATH
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except WebDriverException as e:
        logging.error(f"Failed to initialize WebDriver: {e}")
        print(f"Error: Failed to initialize WebDriver. {e}")
        sys.exit(1)
    
    # Apply stealth techniques to evade detection
    try:
        stealth(driver,
                user_agent=user_agent,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=False,
                run_on_insecure_origins=False,
                )
    except Exception as e:
        logging.error(f"Failed to apply stealth settings: {e}")
        print(f"Error: Failed to apply stealth settings. {e}")
        driver.quit()
        sys.exit(1)
    
    return driver

def verify_login_success(driver):
    """
    Verifies whether the login was successful by locating the profile icon.
    
    Args:
        driver (webdriver.Chrome): Authenticated Selenium WebDriver instance.
    
    Returns:
        bool: True if login is successful, False otherwise.
    """
    try:
        # Primary selector using aria-label
        profile_icon = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//img[@aria-label='Profile picture']"))
        )
        logging.info("Profile icon found using aria-label.")
        return True
    except TimeoutException:
        logging.warning("Profile icon not found using aria-label. Trying alternative selector.")
        try:
            # Alternative selector using alt attribute
            profile_icon = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//img[@alt='Profile picture']"))
            )
            logging.info("Profile icon found using alt attribute.")
            return True
        except TimeoutException:
            logging.error("Profile icon not found using both selectors.")
            return False

def login_instagram(driver):
    """
    Logs into Instagram using provided credentials.
    
    Args:
        driver (webdriver.Chrome): Selenium WebDriver instance.
    """
    try:
        driver.get("https://www.instagram.com/accounts/login/")
        logging.info("Navigated to Instagram login page.")
        print("Navigating to Instagram login page...")
        wait = WebDriverWait(driver, 15)
        
        # Wait for the username input to be present
        username_input = wait.until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_input.clear()
        username_input.send_keys(INSTAGRAM_USERNAME)
        logging.info("Entered username.")
        print("Entered username.")
        time.sleep(random.uniform(1, 3))
        
        # Enter password
        password_input = driver.find_element(By.NAME, "password")
        password_input.clear()
        password_input.send_keys(INSTAGRAM_PASSWORD)
        logging.info("Entered password.")
        print("Entered password.")
        time.sleep(random.uniform(1, 3))
        
        # Submit login form
        password_input.send_keys(Keys.RETURN)
        logging.info("Submitted login form.")
        print("Submitted login form.")
        
        # Wait for login to process
        time.sleep(random.uniform(5, 7))
        
        # Verify login by checking for profile icon
        if verify_login_success(driver):
            logging.info("Logged into Instagram successfully.")
            print("Logged into Instagram successfully.")
        else:
            logging.error("Login might have failed. Profile icon not found.")
            print("Login might have failed. Profile icon not found.")
            # Capture a screenshot for debugging
            driver.save_screenshot("login_failed.png")
            logging.info("Screenshot of failed login saved as 'login_failed.png'.")
            print("Screenshot of failed login saved as 'login_failed.png'.")
            driver.quit()
            sys.exit(1)
    
    except Exception as e:
        logging.error(f"An error occurred during login: {e}")
        print(f"An error occurred during login: {e}")
        # Capture a screenshot for debugging
        driver.save_screenshot("login_error.png")
        logging.info("Screenshot of login error saved as 'login_error.png'.")
        print("Screenshot of login error saved as 'login_error.png'.")
        driver.quit()
        sys.exit(1)

def search_users_by_real_name(driver, real_name, max_results=5):
    """
    Searches for Instagram users by real name.
    
    Args:
        driver (webdriver.Chrome): Authenticated Selenium WebDriver instance.
        real_name (str): The real name to search for.
        max_results (int): Maximum number of usernames to retrieve.
    
    Returns:
        list: List of found usernames.
    """
    search_url = "https://www.instagram.com/explore/search/"
    try:
        driver.get(search_url)
        logging.info(f"Navigated to search page for '{real_name}'.")
        print(f"Navigating to search page for '{real_name}'...")
        
        # Wait for the search input to be present
        wait = WebDriverWait(driver, 15)
        search_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search']"))
        )
        
        search_input.clear()
        search_input.send_keys(real_name)
        logging.info(f"Searching for real name: {real_name}")
        print(f"Searching for real name: {real_name}")
        
        # Wait for search suggestions to appear
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='none']//a[contains(@href, '/')]"))
        )
        time.sleep(random.uniform(2, 4))  # Additional short delay if needed
        
        # Fetch search suggestions
        suggestions = driver.find_elements(By.XPATH, "//div[@role='none']//a[contains(@href, '/')]")
        usernames = []
        for suggestion in suggestions:
            href = suggestion.get_attribute('href')
            if href and "/explore/" not in href and "/tags/" not in href:
                username = href.strip('/').split('/')[-1]
                if username not in usernames:
                    usernames.append(username)
                if len(usernames) >= max_results:
                    break
        
        logging.info(f"Found {len(usernames)} usernames for real name '{real_name}': {usernames}")
        print(f"Found {len(usernames)} usernames for real name '{real_name}': {usernames}")
        return usernames
    except TimeoutException:
        logging.error("Timed out waiting for search input to load.")
        print("Timed out waiting for search input to load.")
        return []
    except Exception as e:
        logging.error(f"An error occurred during user search: {e}")
        print(f"An error occurred during user search: {e}")
        return []

def parse_data(username, user_data):
    """
    Parses and extracts relevant data from the JSON response.
    
    Args:
        username (str): Instagram username.
        user_data (dict): JSON data of the user profile.
    
    Returns:
        dict: Parsed user data.
    """
    captions = []
    posts = user_data.get('edge_owner_to_timeline_media', {}).get('edges', [])
    
    for node in posts:
        caption_edges = node.get('node', {}).get('edge_media_to_caption', {}).get('edges', [])
        if caption_edges:
            text = caption_edges[0].get('node', {}).get('text', '')
            if text:
                captions.append(text)
    
    return {
        'name': user_data.get('full_name', ''),
        'category': user_data.get('category_name', ''),
        'followers': user_data.get('edge_followed_by', {}).get('count', 0),
        'posts': captions,
    }

def scrape(driver, username):
    """
    Scrapes data for a single Instagram username.
    
    Args:
        driver (webdriver.Chrome): Authenticated Selenium WebDriver instance.
        username (str): Instagram username to scrape.
    
    Returns:
        dict or None: Parsed user data if successful, else None.
    """
    url = f'https://instagram.com/{username}/?__a=1&__d=dis'
    try:
        driver.get(url)
        logging.info(f"Attempting to access: {driver.current_url}")
        print(f"Attempting to access: {driver.current_url}")
        
        # Wait for the page to load the JSON data
        wait = WebDriverWait(driver, 15)
        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(random.uniform(3, 6))  # Additional delay if necessary
        
        if "login" in driver.current_url.lower():
            logging.warning(f"Failed to retrieve data for '{username}': Redirected to login.")
            print(f"Failed to retrieve data for '{username}': Redirected to login.")
            return None
        else:
            logging.info(f"Successfully accessed profile for '{username}'.")
            print(f"Successfully accessed profile for '{username}'.")
            try:
                # Extract the page source and parse JSON
                resp_body = driver.find_element(By.TAG_NAME, "body").text
                data_json = json.loads(resp_body)
                user_data = data_json.get('graphql', {}).get('user', {})
                
                if user_data:
                    parsed = parse_data(username, user_data)
                    return parsed
                else:
                    logging.warning(f"No user data found for '{username}'.")
                    print(f"No user data found for '{username}'.")
                    return None
            except (NoSuchElementException, json.JSONDecodeError) as e:
                logging.error(f"Error parsing data for '{username}': {e}")
                print(f"Error parsing data for '{username}': {e}")
                return None
    except WebDriverException as e:
        logging.error(f"WebDriver error for '{username}': {e}")
        print(f"WebDriver error for '{username}': {e}")
        return None

def main():
    """
    Main function to handle user input and initiate scraping.
    """
    print("=== Instagram Profile Scraper ===")
    logging.info("=== Instagram Profile Scraper Started ===")
    
    # Initialize WebDriver for login
    driver = prepare_browser(headless=False)
    login_instagram(driver)
    
    # Prompt for real names to search
    print("\n--- User Search ---")
    input_real_names = input("Enter real names to search (separated by commas): ")
    real_names = [name.strip() for name in input_real_names.split(',') if name.strip()]
    
    if not real_names:
        logging.error("No valid real names entered. Exiting.")
        print("No valid real names entered. Exiting.")
        driver.quit()
        sys.exit(1)
    
    # Prompt for maximum results per real name
    try:
        max_results_input = input("Enter maximum number of usernames to retrieve per real name (default 5): ")
        max_results = int(max_results_input) if max_results_input.strip() else 5
    except ValueError:
        max_results = 5
    
    logging.info(f"Real names to search: {real_names}")
    logging.info(f"Maximum results per real name: {max_results}")
    print(f"Searching for real names: {real_names} with max results {max_results}")
    
    output = {}
    
    for real_name in real_names:
        print(f"\nSearching for users with real name '{real_name}'...")
        logging.info(f"Searching for users with real name '{real_name}'.")
        usernames = search_users_by_real_name(driver, real_name, max_results)
        
        if not usernames:
            logging.warning(f"No usernames found for real name '{real_name}'.")
            print(f"No usernames found for real name '{real_name}'.")
            continue
        
        for username in usernames:
            print(f"\nScraping data for '{username}'...")
            logging.info(f"Scraping data for '{username}'.")
            data = scrape(driver, username)
            if data:
                output[username] = data
            # Implement randomized delay between requests to mimic human behavior
            time.sleep(random.uniform(3, 7))  # Random delay between 3 to 7 seconds
    
    driver.quit()
    logging.info("WebDriver closed.")
    
    print("\n=== Scraping Completed ===\n")
    pprint(output)
    logging.info("=== Scraping Completed ===")
    
    # Optional: Save the output to a JSON file
    save_option = input("\nDo you want to save the output to 'output.json'? (y/n): ").strip().lower()
    if save_option == 'y':
        try:
            with open('output.json', 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=4)
            print("Data successfully saved to 'output.json'.")
            logging.info("Data successfully saved to 'output.json'.")
        except IOError as e:
            logging.error(f"Error saving data to file: {e}")
            print(f"Error saving data to file: {e}")

if __name__ == '__main__':
    main()
