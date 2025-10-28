#!/usr/bin/env python3
"""
Gym-slot reservation bot.
Runs headless Chrome on Linux, logs in, navigates to tomorrow’s schedule,
and books the first free slot.
Tested on Ubuntu 22.04 + Chromium 119.
"""
import datetime as dt
import os
import logging
import traceback
import sys
# import json

from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

LOG = logging.getLogger("gymbot")


def installFirefoxDriver():
    # Create a Service object with the path to GeckoDriver
    service = Service(GeckoDriverManager().install())

    # Pass the Service object to the Firefox webdriver
    driver = webdriver.Firefox(service=service)

    driver.get("https://www.google.com")
    print(driver.title)
    # driver.quit()'


# installFirefoxDriver()

# ---------- CONFIGURATION ----------
GYM_URL = os.getenv("GYM_URL") or "https://masomo3.kyu.ac.ke/my/"
USERNAME = os.getenv("GYM_USER") or "PA106/G/17559/22"
PASSWORD = os.getenv("GYM_PASS") or "40756640"
# unused, just documentation
TIME_TO_RUN = os.getenv("TIME_TO_RUN") or "11:00"
# -----------------------------------


def get_tomorrow_date_str():
    """Return yyyy-mm-dd for tomorrow."""
    return (dt.date.today() + dt.timedelta(days=1)).strftime("%Y-%m-%d")


def build_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")

    driver = webdriver.Firefox(options=opts)
    driver.set_window_size(1200, 800)
    return driver


def login(driver):
    driver.get(GYM_URL)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "username"))
    ).send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "loginbtn").click()
    WebDriverWait(driver, 15).until(EC.url_changes(GYM_URL))
    LOG.info("Logged in")


def book_first_free_slot(driver):
    tomorrow = get_tomorrow_date_str()
    driver.get(f"https://your-school-gym.com/schedule?date={tomorrow}")
    slots = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".slot.available"))
    )
    if not slots:
        LOG.warning("No free slots found")
        return
    slots[0].click()
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "confirm-booking"))
    ).click()
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".success"))
    )
    LOG.info("Slot booked successfully")


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(
            "./gym-bot.log"), logging.StreamHandler()],
    )
    driver = None
    try:
        driver = build_driver()
        login(driver)
        # book_first_free_slot(driver)
    except Exception:
        LOG.error("Booking failed: %s", traceback.format_exc())
        sys.exit(1)
    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass


def cli():
    pass


if __name__ == "__main__":
    main()
