from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from dotenv import load_dotenv
import os
import sys

# STEP 0: Load credentials from .env
load_dotenv()
EMAIL = os.getenv("DEPUTY_EMAIL")
PASSWORD = os.getenv("DEPUTY_PASSWORD")

# STEP 1: Suppress TensorFlow/Chrome/Selenium logs
chrome_service = ChromeService(log_path='NUL' if sys.platform == "win32" else "/dev/null")

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--log-level=3")

driver = webdriver.Chrome(service=chrome_service, options=options)

try:
    # STEP 2: Open login page
    driver.get("https://once.deputy.com/my/login?redirect_url=https%3A%2F%2Fvr.au.deputy.com&redirect_to_instance=1")
    print("🌐 Opened login page.")

    # STEP 3: Enter email
    email_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "login-email"))
    )
    email_input.clear()
    email_input.send_keys(EMAIL)
    print("✉️ Email entered.")

    # STEP 4: Enter password
    password_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "login-password"))
    )
    password_input.clear()
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)
    print("🔑 Password entered and submitted.")
    driver.save_screenshot("logs/headless_debug.png")

    # STEP 5: Click 'Start Shift'
    start_shift_btn = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-success.js-myWeek-Start-Unrostered"))
    )
    start_shift_btn.click()
    print("▶️ 'Start Shift' button clicked.")

    # STEP 6: Open area dropdown
    dropdown = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.select2-container#s2id_shift-modal-unscheduled-area > a.select2-choice"))
    )
    dropdown.click()
    print("🔽 Dropdown clicked.")

    # STEP 7: Select the warehouse
    warehouse_option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//li[contains(@class,'select2-result') and contains(., '[TWT] VR Distribution Camden Park Warehouse')]"
        ))
    )
    warehouse_option.click()
    print("✅ Selected '[TWT] VR Distribution Camden Park Warehouse'.")

    # STEP 8: Click modal start shift button
    modal_start_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "shift-modal-unscheduled-start"))
    )
    WebDriverWait(driver, 10).until(lambda d: modal_start_btn.is_enabled())
    modal_start_btn.click()
    print("🚀 'Start Shift' clicked.")

except Exception as e:
    print("❌ Error:", e)
    driver.save_screenshot("logs/error_screenshot.png")
    with open("logs/error_page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

finally:
    driver.quit()
