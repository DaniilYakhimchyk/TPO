import os
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome(options=options)
    browser.get(BASE_URL)
    yield browser
    browser.quit()


def test_page_heading(driver):
    assert driver.find_element(By.TAG_NAME, "h1").text == "Contact Us"


def test_form_has_required_fields(driver):
    assert driver.find_element(By.ID, "name").is_displayed()
    assert driver.find_element(By.ID, "email").is_displayed()


def test_submit_button_text(driver):
    assert driver.find_element(By.ID, "submit-btn").text == "Send"


def test_form_submit_shows_message(driver):
    driver.find_element(By.ID, "name").send_keys("Test User")
    driver.find_element(By.ID, "email").send_keys("test@example.com")
    driver.find_element(By.ID, "submit-btn").click()
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element(
            (By.ID, "message"), "Message sent successfully!"
        )
    )
    assert (
        driver.find_element(By.ID, "message").text
        == "Message sent successfully!"
    )
