from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from io import BytesIO
import requests
from PIL import Image, ImageTk
import pandas as pd

def scrape_website():
    # Path to your Edge WebDriver executable
    webdriver_path = 'C:/Users/ASUS/Downloads/edgedriver_win64/msedgedriver.exe'

    # Get the URL from the entry widget
    url = url_entry.get()

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

        # Extract user name, item name, and phone numbers from the page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        user_name = soup.find('div', class_='contact-name--m97Sb').text.strip()
        item_name = soup.find('h1', class_='title--3s1R8').text.strip()
        phone_numbers = [phone.text.strip() for phone in soup.find_all('div', class_='phone-numbers--2COKR')]
        subtitle = soup.find('div', class_='subtitle-wrapper--1M5Mv').text.strip()
        
        # Display user name, item name, phone numbers, posted time, and address details in a message box
        user_info = f"User Name: {user_name}\nItem Name: {item_name}\nPhone Numbers:\n" + '\n'.join(phone_numbers) + f"\n{subtitle}"
        messagebox.showinfo("User Information", user_info)

        # Load existing data from the Excel file
        try:
            existing_data = pd.read_excel("scraped_data.xlsx")
        except FileNotFoundError:
            existing_data = pd.DataFrame()

        # Append the new data to the existing data
        new_data = {
            "User Name": user_name,
            "Item Name": item_name,
            "Phone Numbers": ", ".join(phone_numbers),
            "Subtitle": subtitle
        }
        new_data_df = pd.DataFrame([new_data])
        updated_data = pd.concat([existing_data, new_data_df], ignore_index=True)

        # Save the updated data back to the Excel file
        updated_data.to_excel("scraped_data.xlsx", index=False)
        
    except Exception as e:
        messagebox.showerror("Error", str(e))

    # Close the WebDriver
    driver.quit()

    # Reset the loading animation
    loading_label.pack_forget()
    scrape_button.pack(side=LEFT)

def show_loading():
    scrape_button.pack_forget()
    loading_label.pack(side=LEFT)

    root.update()

    scrape_website()

def on_ok():
    # Reset the button state
    scrape_button.pack(side=LEFT)

# Create the main window
root = Tk()
root.title("Web Scraper")

# Create a label and an entry widget for the URL
url_label = Label(root, text="Enter URL:")
url_label.pack()

url_entry = Entry(root, width=50)
url_entry.pack()

# Load the loading animation GIF
loading_url = "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif"
response = requests.get(loading_url)
loading_gif = Image.open(BytesIO(response.content))
loading_gif = loading_gif.convert("RGBA")  # Convert the image to RGBA mode
loading_gif = loading_gif.resize((80, 80), Image.LANCZOS)  # Resize the image using LANCZOS filter
loading_gif = ImageTk.PhotoImage(loading_gif)

# Create a label for the loading animation
loading_label = Label(root, image=loading_gif)

# Create a button to trigger the scraping
scrape_button = Button(root, text="Scrape Website", command=show_loading)
scrape_button.pack(side=LEFT)

# Run the main event loop
root.mainloop()