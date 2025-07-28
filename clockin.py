from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
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

LOG_DIR = "logs"
SCREENSHOT_PATH = os.path.join(LOG_DIR, "error_screenshot.png")
HTML_PATH = os.path.join(LOG_DIR, "error_page.html")

# Ensure logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)

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

# STEP 1: Set up Chrome driver
chrome_service = ChromeService(log_path='NUL' if sys.platform == "win32" else "/dev/null")

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Uncomment to run headless
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
    email_input = WebDriverWait(driver, 0.5).until(
        EC.element_to_be_clickable((By.ID, "login-email"))
    )
    email_input.clear()
    email_input.send_keys(EMAIL)
    print("✉️ Email entered.")

    # STEP 4: Enter password
    password_input = WebDriverWait(driver, 0.5).until(
        EC.element_to_be_clickable((By.ID, "login-password"))
    )
    password_input.clear()
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)
    print("🔑 Password entered and submitted.")

    # STEP 5: Click 'Start Shift'
    try:
        start_shift_btn = WebDriverWait(driver, 0.5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-success.js-myWeek-startShift"))
        )
        start_shift_btn.click()
        print("▶️ 'Start Shift' button clicked.")
    except Exception as e:
        print("❌ Could not find or click 'Start Shift' button:", e)
        driver.save_screenshot(SCREENSHOT_PATH)
        with open(HTML_PATH, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        send_error_email(f"Could not find or click 'Start Shift': {e}", SCREENSHOT_PATH)
        sys.exit(1)

except Exception as e:
    print("❌ Error:", e)
    driver.save_screenshot(SCREENSHOT_PATH)
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    send_error_email(str(e), SCREENSHOT_PATH)
    sys.exit(1)

finally:
    driver.quit()
