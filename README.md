# Clockin - My boss told me to clock in so, I automated it.

My boss told me that if I don’t clock in, I won’t get paid for the day. And with my ADHD brain, I know I’ll forget some days. So, I decided to automate it.

---

## The Plan

Automate the whole clock-in and clock-out process using Python and run it on a Old Laptop.

- ✅ Login to [Deputy](https://www.deputy.com)
- ✅ Click "Start Shift" at 8:55 AM
- ✅ Click "End Shift" at 5:00 PM
- ✅ Never forget again  
- ✅ Actually get paid

---

## Why an Old Laptop?

I could’ve used my PC or phone but let’s be real, they’re not always on.
Then I remembered the dusty old laptop sitting in a drawer, still clinging to life. It’s not good for much these days but it can open a browser and tell my boss I showed up to work.

---

## The Tech Stack
- 🐍 **Python** – scripting brains
- 🧪 **Selenium** – to control the browser like a sleep-deprived intern
- 🌐 **Chrome + ChromeDriver** – the actual browser doing the clicking
- 🔐 **python-dotenv** – keeps my email & password out of the script
- 🕰️ **cron** – so it runs itself every weekday, like magic
- 💻 **Old Laptop** – my dusty, half-retired, always-on automation sidekick

---

## Problems I Expected (and still might get)

- **Headless Mode Drama** – ~~If Deputy’s site doesn’t load right without a screen, I might need to fake one using `xvfb`.~~ Just don't use headless mode.
- **UI Changes** – If they redesign the button I click, everything breaks.
- **Internet** – No Wi-Fi? No paycheck.

---

## Setup (aka: How to Clone My Laziness)

1. Install dependencies:
    ```bash
    pip install selenium python-dotenv
    ```

2. Create a `.env` file:
    ```env
    DEPUTY_EMAIL=you@example.com
    DEPUTY_PASSWORD=SuperSecret123

    ALERT_EMAIL_FROM=your_email@gmail.com
    ALERT_EMAIL_PASSWORD=your_app_password
    ALERT_EMAIL_TO=your_email@gmail.com
    SMTP_SERVER=smtp.gmail.com
    SMTP_PORT=587
    ```

3. Add two cronjobs:
    ```cron
    # Clock in at 8:55 AM
    55 8 * * 1-5 /usr/bin/python3 /home/username/clockin/clockin.py --start

    # Clock out at 5:00 PM
    0 17 * * 1-5 /usr/bin/python3 /home/username/clockin/clockout.py --end
    ```

---

## Future Plans

- Add a web interface to manage users (like a real app)
- Log shift data somewhere
- ~~Make it yell at me if it fails~~ ✅ It emails me now if something breaks

---
