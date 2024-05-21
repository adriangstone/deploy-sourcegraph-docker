#!/usr/bin/env python3
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

def setup_sourcegraph_admin_account():
    print("Initialize a WebDriver (Firefox in headless mode)")
    firefox_options = Options()
    firefox_options.headless = True  # Run headless mode
    firefox_options.add_argument("--disable-gpu")  # Disable GPU acceleration if needed

    browser = webdriver.Firefox(options=firefox_options)

    try:
        print("Open the Sourcegraph setup page")
        url = "http://0.0.0.0"
        browser.get(url)

        # Ensure the page is fully loaded
        WebDriverWait(browser, 10).until(lambda driver: driver.execute_script("return document.readyState") == "complete")

        print("Wait for the page to load and locate the form fields")
        wait = WebDriverWait(browser, 10)
        email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
        username_field = browser.find_element(By.ID, "username")
        password_field = browser.find_element(By.ID, "password")

        print("Fill in the email, username, and password fields")
        admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
        admin_username = os.getenv("ADMIN_USERNAME", "admin")
        admin_password = os.getenv("ADMIN_PASSWORD", "adminadminadmin")

        email_field.send_keys(admin_email)
        username_field.send_keys(admin_username)
        password_field.send_keys(admin_password)

        # Use JavaScript to submit the form directly
        print("Submitting the form using JavaScript")
        submit_button = browser.find_element(By.XPATH, "//button[@type='submit']")
        time.sleep(5)
        browser.execute_script("arguments[0].click();", submit_button)

        browser.save_screenshot("debug_screenshot_before_wait.png")

        # Optionally, wait for a response or a new page
        WebDriverWait(browser, 100).until(EC.url_changes(url))

        # Capture screenshot after attempting to submit
        browser.save_screenshot("debug_screenshot_after_submit.png")

    finally:
        print("Close the WebDriver")
        time.sleep(10)    
        browser.quit()

if __name__ == "__main__":
    setup_sourcegraph_admin_account()