from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Path to your Edge WebDriver executable
webdriver_path = 'C:/Users/ASUS/Downloads/edgedriver_win64/msedgedriver.exe'

# URL of the website you want to scrape
url = 'https://ikman.lk/en/ad/mg-zs-jeep-for-rent-for-sale-colombo-23'

# Configure Edge options
options = Options()
options.use_chromium = True  # Use the Chromium-based Edge browser
options.add_argument('--headless')  # Run Edge in headless mode (without GUI)
options.add_argument('--disable-gpu')  # Disable GPU acceleration

# Initialize Edge WebDriver
service = Service(webdriver_path)
driver = webdriver.Edge(service=service, options=options)

# Load the website
driver.get(url)

# Wait for the button to appear and click it
try:
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'contact-section--1qlvP'))
    )
    button.click()
    time.sleep(2)  # Wait for the phone numbers to appear (adjust as needed)
    
    # Extract all phone numbers from the page source
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    phone_numbers = [phone.text.strip() for phone in soup.find_all('div', class_='phone-numbers--2COKR')]
    print('Phone numbers:', phone_numbers)
except Exception as e:
    print('Error:', e)

# Close the WebDriver
driver.quit()
