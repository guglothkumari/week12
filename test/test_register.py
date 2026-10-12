import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager
import time

@pytest.fixture
def setup_teardown():
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    yield driver
    driver.quit()

def get_alert_text(driver):
    alert = Alert(driver)
    text = alert.text
    alert.accept()
    return text

def test_empty_name(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")  # Replace with the actual URL of your Flask app
    driver.find_element(By.ID, "name").clear()
    driver.find_element(By.ID, "password").send_keys("testpassword")
    driver.find_element(By.ID, "submit").click ()

    time.sleep(1)
    alert_text = get_alert_text(driver)
    assert alert_text == "UserName cannot be empty."

def test_empty_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")  # Replace with the actual URL of your Flask app
    driver.find_element(By.ID, "name").send_keys("testuser")
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "submit").click ()

    time.sleep(1)
    alert_text = get_alert_text(driver)
    assert alert_text == "Password cannot be empty."

def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")  # Replace with the actual URL of your Flask app
    driver.find_element(By.ID, "name").send_keys("testuser")
    driver.find_element(By.ID, "password").send_keys("123")
    driver.find_element(By.ID, "submit").click ()

    time.sleep(1)
    alert_text = get_alert_text(driver)
    assert alert_text == "Password must be at least 6 characters long."

def test_valid_registration(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")  # Replace with the actual URL of your Flask app
    driver.find_element(By.ID, "name").send_keys("testuser")
    driver.find_element(By.ID, "password").send_keys("testpassword")
    driver.find_element(By.ID, "submit").click()

    time.sleep(1)
    current_url = driver.current_url
    assert "/submit" in current_url, f"Expected to be redirected to /submit, but got {current_url}"
    body = driver.find_element(By.TAG_NAME, "body").text
    assert "Registration Successful" in body.text, f"Expected success message not found on the page{body.text}."
