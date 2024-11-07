from selenium import webdriver
from selenium.webdriver.common.by import By
import time, random, string
from selenium.common.exceptions import NoSuchElementException


def login(driver):
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//a[@class = 'text-sm text-gray-700 underline']").click()
    time.sleep(1)
    valid_email = "abcxyz544000@gmail.com"
    valid_pass = "abcxyz544000"
    driver.find_element(By.ID, "email").send_keys(valid_email)
    driver.find_element(By.ID, "password").send_keys(valid_pass)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)

def login_admin(driver):
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//a[@class = 'text-sm text-gray-700 underline']").click()
    time.sleep(1)
    valid_email = "congdanhabc@outlook.com.vn"
    valid_pass = "danh5112003"
    driver.find_element(By.ID, "email").send_keys(valid_email)
    driver.find_element(By.ID, "password").send_keys(valid_pass)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)

def delete_all_product_in_cart(driver):
    driver.find_element(By.XPATH, "//a[@href = '/cart']").click()
    out_of_product = False
    while not out_of_product: 
        try:
            time.sleep(1)
            driver.find_element(By.XPATH, '//button[@class = "btn btn-danger btn-sm remove-from-cart"]').click()
            time.sleep(1)
            alert = driver.switch_to.alert 
            alert.accept()
        except NoSuchElementException:
            out_of_product = True


def add_random_product(driver):
    driver.find_element(By.XPATH, "//a[text()='Menu']").click()
    time.sleep(1)
    random_product = random.randint(3, 8)
    product_list = {}
    for i in range(random_product):
        tr_elements = driver.find_elements(By.XPATH, "//tbody/tr")
        pick = False
        while not pick:
            tr_element = random.choice(tr_elements)
            p_name = tr_element.find_element(By.TAG_NAME, "h2").text
            try: 
                if bool(next((product_name for product_name in product_list.keys() if product_name == p_name), "")):
                    continue
            except AttributeError:
                a=0
            try: 
                add_button = tr_element.find_element(By.XPATH, ".//button[text() = 'Add to Cart']")
                pick = True
                price = float(tr_element.find_element(By.TAG_NAME, "h4").text[1:])
                quan = random.randint(1, 10)
                input_e = tr_element.find_element(By.ID, "myNumber")
                input_e.clear()
                input_e.send_keys(quan)
                add_button.click()
                product_list[p_name] = [price, quan]
            except NoSuchElementException: 
                a=0
            time.sleep(1)
    return product_list

def generate_random_string(length):
    # Chọn ngẫu nhiên các ký tự từ chữ cái và số
    letters_and_digits = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters_and_digits) for i in range(length))
    return random_string