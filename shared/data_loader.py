import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

# Create the download directory if it doesn't exist
download_dir = "C:/Users/Biebert/Downloads"
os.makedirs(download_dir, exist_ok=True)

# Initialize Selenium WebDriver
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": os.path.abspath(download_dir),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scroll_to_bottom(driver):
    """Scroll to the bottom of the page."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  # Break if no new content is loaded
            break
        last_height = new_height

try:
    # Open the target website
    url = "https://www.pedestrian.melbourne.vic.gov.au/#date=25-11-2024&sensor=AlfPl_T&time=1"
    driver.get(url)
    print(f"Opened {url}")
    print('_' * 30)
    wait = WebDriverWait(driver, 20)
    time.sleep(5)  # Allow time for the page to load

    # Scroll to the bottom of the page to load all links
    print("Scrolling to load all links...")
    scroll_to_bottom(driver)

    # Fetch all CSV links after scrolling
    csv_links = driver.find_elements(By.XPATH, '//a[contains(@href, ".csv")]')
    print(f"Found {len(csv_links)} CSV files on the page")
    print('_' * 30)

    # Iterate over links and click each one to trigger download
    for index, link in enumerate(csv_links):  # Process all links
        for attempt in range(3):  # Retry up to 3 times if stale element
            try:
                print(f"Clicking on CSV file {index + 1}/{len(csv_links)}")
                
                # Scroll the link into view and click it
                driver.execute_script("arguments[0].scrollIntoView(true);", link)
                link.click()
                time.sleep(2)  # Allow time for the download to initiate
                break  # Exit retry loop if successful
            except StaleElementReferenceException:
                print(f"Stale element encountered. Retrying {attempt + 1}/3...")
                # Re-fetch the link if it becomes stale
                link = wait.until(EC.presence_of_element_located((By.XPATH, f'(//a[contains(@href, ".csv")])[{index + 1}]')))

finally:
    input("Press Enter to close the browser...")
    print("Closing the browser...")
    print('_' * 30)
    driver.quit()

print(f"All files downloaded to {download_dir}")
