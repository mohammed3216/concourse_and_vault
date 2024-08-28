from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import os
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

current_dir = os.getcwd()
prefs = {
    "download.default_directory": current_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

service = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

def login(username, password):
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "account", " " ))]'))
    )
    login_button.click()

    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[(@id = "id_username")]'))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[(@id = "id_password")]'))
    )

    email_input.send_keys(username)
    password_input.send_keys(password)

    second_login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "icon-user", " " ))]'))
    )
    second_login_button.click()

def download_and_process_data(company_url, company_name):
    driver.get(company_url)
    
    # Wait for the export button to be clickable
    export = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "icon-download", " " ))]'))
    )
    export.click()
    
    # Wait for the download to complete
    time.sleep(10)
    
    # Read Excel file into pandas DataFrame
    df = pd.read_excel(f"{company_name}.xlsx", sheet_name="Data Sheet")
    
    # Select rows and columns
    df = df.iloc[14:30, :11]
    
    # Print resulting DataFrame
    print(df)
    
    # Load the DataFrame into the PostgreSQL database
    df.to_sql(f'{company_name}_data', engine, if_exists='replace', index=False)

# Login once
login("firstscreener123@gmail.com", "Asdf!234")

# List of companies with their corresponding URLs
companies = {
    "Reliance": "https://www.screener.in/company/RELIANCE/consolidated/",
    "TCS": "https://www.screener.in/company/TCS/consolidated/",
    "Infosys": "https://www.screener.in/company/INFY/consolidated/"
    # Add more companies here
}

db_host = "192.168.3.59"
db_name = "reliance"
db_user = "mdop"
db_password = "password"
db_port = "5432"

# Create the database engine
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Iterate over the companies and process each one
for company_name, company_url in companies.items():
    download_and_process_data(company_url, company_name)

# Close the browser
driver.quit()
