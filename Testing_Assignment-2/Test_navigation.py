import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, requests
from condition_function import *

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

#Testcase 1
def test_navigation_menu(driver):
    #condition
    login(driver)

    #main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    header = driver.find_element(By.TAG_NAME, "header")
    nav_list = header.find_elements(By.CLASS_NAME, "scroll-to-section")
    check_link_response = True
    count = 0
    for nav in nav_list:
        # Lấy URL của thẻ <a>
        a_element = nav.find_element(By.TAG_NAME, "a")
        name = a_element.text
        link_url = a_element.get_attribute("href")

        # Sử dụng thư viện requests để kiểm tra mã phản hồi HTTP
        response = requests.get(link_url)
        response_code = response.status_code
        if response_code == 200:
            check_link_response = check_link_response and True
            count += 1
        else:
            check_link_response = check_link_response and False
        print(f"Response code - {name}: {response_code} - {check_link_response}")
    
    if check_link_response == True:
        for i in range(count-1, -1, -1):
            # Lấy URL của thẻ <a>
            header = driver.find_element(By.TAG_NAME, "header")
            nav_list = header.find_elements(By.CLASS_NAME, "scroll-to-section")
            nav_list[i].find_element(By.TAG_NAME, "a").click()
            time.sleep(2)
    assert check_link_response
        
#Testcase 2
def test_navigation_logo(driver):
    #main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    header = driver.find_element(By.TAG_NAME, "header")
    logo_element = header.find_element(By.CLASS_NAME, "logo")
    link_url = logo_element.get_attribute("href")
    check_link_response = True
    # Sử dụng thư viện requests để kiểm tra mã phản hồi HTTP
    response = requests.get(link_url)
    response_code = response.status_code
    if response_code == 200:
        check_link_response = check_link_response and True
    else:
        check_link_response = check_link_response and False
    print(f"Response code - logo: {response_code} - {check_link_response}")
    logo_element.click()
    time.sleep(3)
    
    assert check_link_response



#pytest -s Test_navigation.py
#2 Testcase