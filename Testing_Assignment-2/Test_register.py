import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, random
from selenium.common.exceptions import StaleElementReferenceException
from condition_function import *


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

#Testcase 1
def test_register_success(driver):
    #main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[text()='Register']").click()

    time.sleep(1)
    name = generate_random_string(8)
    email = generate_random_string(5) + '@gmail.com'
    number = ''.join(random.choice(string.digits) for i in range(10))
    password = generate_random_string(12)
    
    driver.find_element(By.ID, "name").send_keys(name)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "phone").send_keys(number)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "password_confirmation").send_keys(password)
    time.sleep(2)
    driver.find_element(By.TAG_NAME, "button").click()

    time.sleep(2)
    assert "login" in driver.current_url

#Testcase 2
def test_register_blank_name_input(driver):
    #main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[text()='Register']").click()

    time.sleep(1)
    email = generate_random_string(5) + '@gmail.com'
    number = ''.join(random.choice(string.digits) for i in range(10))
    password = generate_random_string(12)
    
    name_input = driver.find_element(By.ID, "name")
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "phone").send_keys(number)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "password_confirmation").send_keys(password)
    time.sleep(1)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    #Check blank input
    check_blank = None
    try:
        check_blank = name_input.get_attribute("validationMessage")
        print("Blank error is: ", check_blank)
    except StaleElementReferenceException: 
        print("Blank error is displayed unsuccessfully")
    time.sleep(2)
 
    assert check_blank is not None

#Testcase 3
def test_register_blank_email_input(driver):
    #main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[text()='Register']").click()

    time.sleep(1)
    name = generate_random_string(8)
    number = ''.join(random.choice(string.digits) for i in range(10))
    password = generate_random_string(12)
    
    driver.find_element(By.ID, "name").send_keys(name)
    email_input = driver.find_element(By.ID, "email")
    driver.find_element(By.ID, "phone").send_keys(number)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "password_confirmation").send_keys(password)
    time.sleep(1)
    driver.find_element(By.TAG_NAME, "button").click()
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
def test_register_invalid_format_email_input(driver):
    #main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[text()='Register']").click()

    time.sleep(1)
    name = generate_random_string(8)
    number = ''.join(random.choice(string.digits) for i in range(10))
    password = generate_random_string(12)
    
    driver.find_element(By.ID, "name").send_keys(name)
    email_input = driver.find_element(By.ID, "email")
    driver.find_element(By.ID, "phone").send_keys(number)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "password_confirmation").send_keys(password)
    time.sleep(1)

    email = generate_random_string(6)
    email_input.send_keys(email)
    driver.find_element(By.TAG_NAME, "button").click()
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

#Testcase 5
def test_register_exceed_email_input(driver):
    #main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[text()='Register']").click()

    time.sleep(1)
    name = generate_random_string(8)
    number = ''.join(random.choice(string.digits) for i in range(10))
    password = generate_random_string(12)
    
    driver.find_element(By.ID, "name").send_keys(name)
    email_input = driver.find_element(By.ID, "email")
    driver.find_element(By.ID, "phone").send_keys(number)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "password_confirmation").send_keys(password)
    time.sleep(1)

    email = generate_random_string(1000) + "@gmail.com"
    email_input.send_keys(email)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    #Check exceeded character count
    check_exceed = None
    try:
        check_exceed = email_input.get_attribute("validationMessage")
        print("Exceed error is: ", check_exceed)
    except StaleElementReferenceException: 
        print("Exceed error is displayed unsuccessfully")
    time.sleep(2)
    
    assert check_exceed is not None


#pytest -s Test_register.py
#5 Testcase