from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def travellingMerchantScript():
    # Configure Firefox options for headless mode
    options = Options()
    options.add_argument("--headless")

    # Initialize the Firefox WebDriver with options
    driver = webdriver.Firefox(options=options)

    # Set the window size to a larger resolution
    driver.set_window_size(800, 1080)

    try:
        # Navigate to the URL
        driver.get("https://runescape.wiki/w/Travelling_Merchant%27s_Shop")

        # Wait for the element to load
        wait = WebDriverWait(driver, 10)
        shop_table = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[5]')))

        # Capture screenshot of the web element
        screenshot_path = os.path.expanduser("data/merchant_stock.png")
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        shop_table.screenshot(screenshot_path)

        print(f"Screenshot saved at: {screenshot_path}")

    finally:
        # Close the browser
        driver.quit()
