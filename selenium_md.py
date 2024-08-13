# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import os

# # Setup Chrome options
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)

# # Path to your chromedriver executable
# webdriver_service = Service('C:/Users/Ashraf Sunesara/Downloads/chromedriver-win64/chromedriver.exe')

# # Initialize WebDriver
# driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# try:
#     # Define URLs
#     login_url = 'https://www.screener.in/login/'
#     company_url = 'https://www.screener.in/company/RELIANCE/consolidated/'

#     # Navigate to login page
#     driver.get(login_url)
#     time.sleep(2)  # Wait for page to load

#     # Perform login
#     email = "35mk8vkgf@rskfc.com"
#     password = "password@123"

#     driver.find_element(By.NAME, 'username').send_keys(email)
#     driver.find_element(By.NAME, 'password').send_keys(password)
#     driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
#     time.sleep(5)  # Wait for login to process

#     if "Logout" in driver.page_source:
#         print("Login successful")

#         # Navigate to company page
#         driver.get(company_url)
#         time.sleep(5)  # Wait for page to load

#         # Debugging: Take a screenshot before looking for the button
#         driver.save_screenshot('pre_click_screenshot.png')

#         # Try finding the Export button
#         try:
#             export_button = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[download="RELIANCE-Consolidated.xlsx"]'))
#             )
#             export_button.click()
#             time.sleep(5)  # Wait for download to start

#             # Check for download completion
#             download_dir = os.path.expanduser("~") + "/Downloads/"
#             files = [f for f in os.listdir(download_dir) if f.endswith('.xlsx')]
#             if files:
#                 print("Excel file downloaded successfully.")
#             else:
#                 print("Failed to download the file.")
#         except Exception as e:
#             print(f"Error finding or clicking the export button: {e}")
#     else:
#         print("Login failed.")
# finally:
#     driver.quit()





from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime
 
# Login credentials
usernames = ["35mk8vkgf@rskfc.com"]
passwords = ["password@123"]
 
def login_and_download_file(url, username, password, file_suffix):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
 
    try:
        # Log in
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "account", " " ))]'))
        ).click()
 
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[(@id = "id_username")]'))
        )
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[(@id = "id_password")]'))
        )
 
        email_input.send_keys(username)
        password_input.send_keys(password)
 
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "icon-user", " " ))]'))
        ).click()
 
        # Navigate to the desired page
        driver.get("https://www.screener.in/company/RELIANCE/consolidated/")
       
        # Wait for the download button to be clickable and click it
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[3]/div[1]/form/button'))
        )
        download_button.click()
 
        # Wait for download to complete (or check for a file download indication)
        WebDriverWait(driver, 30).until(EC.staleness_of(download_button))  # Wait until the button is no longer clickable
 
    finally:
        driver.quit()
 
# if __name__ == '__main__':
#     for i, (username, password) in enumerate(zip(usernames, passwords)):
#         login_and_download_file("https://www.screener.in/", username, password, i)
 
