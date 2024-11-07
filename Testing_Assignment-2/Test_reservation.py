import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, random
from condition_function import *
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

#Testcase 1
def test_reservation_login(driver):
    #condition
    login(driver)

    #main
    driver.find_element(By.ID, "name").send_keys("customer")
    driver.find_element(By.ID, "email").send_keys("customer@gmail.com")
    driver.find_element(By.ID, "phone").send_keys("09862517818")
    Select(driver.find_element(By.ID, "number-guests")).select_by_value("5")
    driver.find_element(By.ID, "date").send_keys("30.12.2024")
    Select(driver.find_element(By.ID, "time")).select_by_value("Lunch")
    driver.find_element(By.ID, "message").send_keys("abc123")
    driver.find_element(By.ID, "form-submit").click()

    time.sleep(3)
    assert driver.find_element(By.TAG_NAME, "h1").text == "Success"

#Testcase 2
def test_reservation_no_login(driver):
    #main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.ID, "name").send_keys("customer")
    driver.find_element(By.ID, "email").send_keys("customer@gmail.com")
    driver.find_element(By.ID, "phone").send_keys("09862517818")
    Select(driver.find_element(By.ID, "number-guests")).select_by_value("5")
    driver.find_element(By.ID, "date").send_keys("30.12.2024")
    Select(driver.find_element(By.ID, "time")).select_by_value("Lunch")
    driver.find_element(By.ID, "message").send_keys("abcsysasjdasjkaskd")
    driver.find_element(By.ID, "form-submit").click()

    time.sleep(3)
    assert driver.find_element(By.TAG_NAME, "h1").text == "Success"


#Testcase 3
def test_reservation_blank_email_input(driver):
    #condition
    login(driver)

    #main
    driver.find_element(By.ID, "name").send_keys("customer")
    email_input = driver.find_element(By.ID, "email")
    driver.find_element(By.ID, "phone").send_keys("09862517818")
    Select(driver.find_element(By.ID, "number-guests")).select_by_value("5")
    driver.find_element(By.ID, "date").send_keys("30.12.2024")
    Select(driver.find_element(By.ID, "time")).select_by_value("Lunch")
    driver.find_element(By.ID, "message").send_keys("abcsysasjdasjkaskd")
    driver.find_element(By.ID, "form-submit").click()
    time.sleep(1)

    #Check blank input
    check_blank = None
    try:
        check_blank = email_input.get_attribute("validationMessage")
        print("Blank error is: ", check_blank)
    except StaleElementReferenceException: 
        print("Blank error is displayed unsuccessfully")
    time.sleep(2)

    assert check_blank is not None

#Testcase 4
def test_reservation_invalid_format_email_input(driver):
    #condition
    login(driver)

    #main
    driver.find_element(By.ID, "name").send_keys("customer")
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys("customer")
    driver.find_element(By.ID, "phone").send_keys("09862517818")
    Select(driver.find_element(By.ID, "number-guests")).select_by_value("5")
    driver.find_element(By.ID, "date").send_keys("30.12.2024")
    Select(driver.find_element(By.ID, "time")).select_by_value("Lunch")
    driver.find_element(By.ID, "message").send_keys("abcsysasjdasjkaskd")
    driver.find_element(By.ID, "form-submit").click()
    time.sleep(1)

    #Check email format
    check_format = None
    try:
        check_format = email_input.get_attribute("validationMessage")
        print("Format error is: ", check_format)
    except StaleElementReferenceException: 
        print("Format error is displayed unsuccessfully")
    time.sleep(2)

    assert check_format is not None


#pytest -s Test_reservation.py
#4 testcase 