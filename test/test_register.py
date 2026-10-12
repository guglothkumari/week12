import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# Fixture to open and close the browser
@pytest.fixture
def setup_teardown():
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    yield driver
    driver.quit()


# Function to get and accept JavaScript alert
def get_alert_text(driver):
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = Alert(driver)
    text = alert.text
    alert.accept()
    return text


# Test 1: Empty username
def test_empty_name(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    driver.find_element(By.ID, "name").clear()
    driver.find_element(By.ID, "password").send_keys("testpassword")

    # Allow JavaScript validation to run instead of browser validation
    driver.execute_script(
        "document.querySelector('form').noValidate = true;"
    )

    driver.find_element(By.ID, "submit").click()

    alert_text = get_alert_text(driver)
    assert alert_text == "UserName cannot be empty."


# Test 2: Empty password
def test_empty_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    driver.find_element(By.ID, "name").send_keys("testuser")
    driver.find_element(By.ID, "password").clear()

    # Allow JavaScript validation to run instead of browser validation
    driver.execute_script(
        "document.querySelector('form').noValidate = true;"
    )

    driver.find_element(By.ID, "submit").click()

    alert_text = get_alert_text(driver)
    assert alert_text == "Password cannot be empty."


# Test 3: Password shorter than 6 characters
def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    driver.find_element(By.ID, "name").send_keys("testuser")
    driver.find_element(By.ID, "password").send_keys("123")
    driver.find_element(By.ID, "submit").click()

    alert_text = get_alert_text(driver)
    assert alert_text == (
        "Password must be at least 6 characters long."
    )


# Test 4: Successful registration
def test_valid_registration(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    driver.find_element(By.ID, "name").send_keys("testuser")
    driver.find_element(By.ID, "password").send_keys("testpassword")
    driver.find_element(By.ID, "submit").click()

    # Flask route is /register, not /submit
    WebDriverWait(driver, 5).until(
        EC.url_contains("/register")
    )

    current_url = driver.current_url
    assert "/register" in current_url, (
        f"Expected /register, but got {current_url}"
    )

    body = driver.find_element(By.TAG_NAME, "body").text
    assert "Registration Successful" in body, (
        f"Expected success message not found. Page content: {body}"
    )
