from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def check_email_with_selenium(email):
    driver = webdriver.Chrome()  # Ensure you have the appropriate WebDriver installed
    driver.get("https://haveibeenpwned.com/")
    
    search_box = driver.find_element(By.ID, "Account")
    search_box.send_keys(email)
    search_box.send_keys(Keys.RETURN)
    
    time.sleep(5)  # Wait for results to load
    results = driver.page_source
    driver.quit()
    return results

if __name__ == "__main__":
    email = input("Enter the email address to check: ")
    result = check_email_with_selenium(email)
    print(result)
