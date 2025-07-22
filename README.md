# Clockin - My boss told me to clock in so, I automated it.

My boss told me that if I don’t clock in, I won’t get paid for the day. And with my ADHD brain, I know I’ll forget some days. So, I decided to automate it.

---

## The Plan

Automate the whole clock-in and clock-out process using Python and run it on a Raspberry Pi.

- ✅ Login to [Deputy](https://www.deputy.com)
- ✅ Click "Start Shift" at 8:55 AM
- ✅ Click "End Shift" at 5:00 PM
- ✅ Never forget again  
- ✅ Actually get paid

All hands-free. No coffee needed.

---

## Why a Raspberry Pi?

I could’ve used my PC or phone, but they aren’t *always on*.
My trusty Raspberry Pi 4B is already my media server why cant it also clock me in and out?

---

## The Tech Stack
- 🐍 **Python 3** – scripting brains
- 🧪 **Selenium** – to control the browser like a sleep-deprived intern
- 🌐 **Chromium + ChromeDriver** – the actual browser doing the clicking
- 🔐 **python-dotenv** – keeps my email & password out of the script
- 🕰️ **cron** – so it runs itself every weekday, like magic
- 🍓 **Raspberry Pi 4B** – my always-on automation buddy

---

## Problems I Expected (and still might get)

- **Headless Mode Drama** – If Deputy’s site doesn’t load right without a screen, I might need to fake one using `xvfb`.
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
    ```

3. Add two cronjobs:
    ```cron
    # Clock in at 8:55 AM
    55 8 * * 1-5 /usr/bin/python3 /home/pi/clockin/clockin.py --start

    # Clock out at 5:00 PM
    0 17 * * 1-5 /usr/bin/python3 /home/pi/clockin/clockout.py --end
    ```

---

## Future Plans

- Add a web interface to manage users (like a real app)
- Log shift data somewhere
- Make it yell at me if it fails

---
