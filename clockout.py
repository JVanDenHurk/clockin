from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from dotenv import load_dotenv
import os
import sys
import smtplib
from email.message import EmailMessage

# STEP 0: Load credentials from .env
load_dotenv()
EMAIL = os.getenv("DEPUTY_EMAIL")
PASSWORD = os.getenv("DEPUTY_PASSWORD")

ALERT_EMAIL_FROM = os.getenv("ALERT_EMAIL_FROM")
ALERT_EMAIL_PASSWORD = os.getenv("ALERT_EMAIL_PASSWORD")
ALERT_EMAIL_TO = os.getenv("ALERT_EMAIL_TO")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# STEP 1: Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

def send_error_email(error_message, screenshot_path):
    msg = EmailMessage()
    msg['Subject'] = 'Clockin Script Error Alert'
    msg['From'] = ALERT_EMAIL_FROM
    msg['To'] = ALERT_EMAIL_TO
    msg.set_content(f"Your clockin script failed with the following error:\n\n{error_message}")

    # Attach screenshot
    try:
        with open(screenshot_path, 'rb') as f:
            img_data = f.read()
            msg.add_attachment(img_data, maintype='image', subtype='png', filename='error_screenshot.png')
    except Exception as e:
        print(f"⚠️ Could not attach screenshot: {e}")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(ALERT_EMAIL_FROM, ALERT_EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("📧 Error email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send error email: {e}")

def try_find_click(driver, by, selector, wait_time=0.5):
    try:
        elem = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((by, selector))
        )
        elem.click()
        print(f"✅ Successfully clicked element")
        return True
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
        print(f"⚠️ Failed to find/click element: {e}")
        raise  # Raise exception to signal failure

# STEP 2: Set up Chrome driver
chrome_service = ChromeService(log_path='NUL' if sys.platform == "win32" else "/dev/null")

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Uncomment to run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--log-level=3")

driver = webdriver.Chrome(service=chrome_service, options=options)

try:
    # STEP 3: Open login page
    driver.get("https://once.deputy.com/my/login?redirect_url=https%3A%2F%2Fvr.au.deputy.com&redirect_to_instance=1")
    print("🌐 Opened login page.")

    # STEP 4: Enter email
    email_input = WebDriverWait(driver, 0.5).until(
        EC.element_to_be_clickable((By.ID, "login-email"))
    )
    email_input.clear()
    email_input.send_keys(EMAIL)
    print("✉️ Email entered.")

    # STEP 5: Enter password
    password_input = WebDriverWait(driver, 0.5).until(
        EC.element_to_be_clickable((By.ID, "login-password"))
    )
    password_input.clear()
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)
    print("🔑 Password entered and submitted.")

    # STEP 6: Try clicking "End Shift" and confirm
    try:
        try_find_click(driver, By.CSS_SELECTOR, "button.btn.btn-danger.btn-wide.js-myWeek-endShift")
        try_find_click(driver, By.CSS_SELECTOR, "button.btn.btn-danger.js-MyWeek-Modal-SubmitShift")
    except Exception as e:
        print("❌ Could not find or click 'End Shift' button or confirm modal:", e)
        driver.save_screenshot("logs/error_screenshot.png")
        try:
            with open("logs/error_page.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source or "<empty page source>")
        except Exception as write_error:
            print(f"⚠️ Could not write error_page.html: {write_error}")
        send_error_email(f"Could not click End Shift: {e}", "logs/error_screenshot.png")
        sys.exit(1)

except Exception as e:
    print("❌ General error:", e)
    driver.save_screenshot("logs/error_screenshot.png")
    try:
        with open("logs/error_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source or "<empty page source>")
    except Exception as write_error:
        print(f"⚠️ Could not write error_page.html: {write_error}")
    send_error_email(str(e), "logs/error_screenshot.png")
    sys.exit(1)

finally:
    driver.quit()
