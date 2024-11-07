import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, random, re
from selenium.common.exceptions import NoSuchElementException
from condition_function import *

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


#Testcase 1
def test_add_1_product(driver):
    #condition
    login(driver)
    delete_all_product_in_cart(driver)

    #main
    driver.find_element(By.XPATH, "//a[text()='Menu']").click()
    time.sleep(1)
    tr_elements = driver.find_elements(By.XPATH, "//tbody/tr")
    in_stock = False
    while not in_stock:
        tr_element = random.choice(tr_elements)
        p_name = tr_element.find_element(By.TAG_NAME, "h2").text
        try: 
            add_button = tr_element.find_element(By.XPATH, ".//button[text() = 'Add to Cart']")
            in_stock = True
            price = float(tr_element.find_element(By.TAG_NAME, "h4").text[1:])
            quan = random.randint(1, 10)
            input_e = tr_element.find_element(By.ID, "myNumber")
            input_e.clear()
            input_e.send_keys(quan)
            add_button.click()
            print(p_name, ": ", in_stock, " ", price)
        except NoSuchElementException: 
            print(p_name, ": ", in_stock)
        time.sleep(1)

    driver.find_element(By.XPATH, "//a[@href = '/cart']").click()
    cart_td_elements = driver.find_elements(By.XPATH, "//tbody/tr/td")
    check_name = p_name == cart_td_elements[0].text
    check_price = price == float(cart_td_elements[1].text[1:])
    check_quan = quan == float(cart_td_elements[2].text)
    check_sub_total = (price * quan) == float(cart_td_elements[3].text[1:])
    print(f"Check name: {p_name} - {check_name}")
    print(f"Check price: {price} - {check_price}")
    print(f"Check quantity: {quan} - {check_quan}")
    print(f"Check sub_total: {price * quan} - {check_sub_total}")
    
    time.sleep(5)
    assert check_name and check_price and check_quan and check_sub_total

#Testcase 2
def test_add_negative_quantity_to_cart(driver):
    #condition
    login(driver)
    delete_all_product_in_cart(driver)
    
    #main
    driver.find_element(By.XPATH, "//a[text()='Menu']").click()
    time.sleep(1)
    tr_elements = driver.find_elements(By.XPATH, "//tbody/tr")
    in_stock = False
    while not in_stock:
        tr_element = random.choice(tr_elements)
        try: 
            add_button = tr_element.find_element(By.XPATH, ".//button[text() = 'Add to Cart']")
            in_stock = True
            quan = -1
            input_e = tr_element.find_element(By.ID, "myNumber")
            input_e.clear()
            input_e.send_keys(quan)
            add_button.click()
            error_message = driver.find_element(By.CSS_SELECTOR, "input:invalid")
            check_negative = error_message is not None
            if check_negative:
                print("Error is displayed successfully") 
        except NoSuchElementException: 
            print("Error is displayed unsuccessfully")
        time.sleep(1)
    
    driver.find_element(By.XPATH, "//a[@href = '/cart']").click()

    time.sleep(5)
    assert check_negative


#Testcase 3
def test_add_multiple_product(driver):
    #condition
    login(driver)
    delete_all_product_in_cart(driver)

    #main
    driver.find_element(By.XPATH, "//a[text()='Menu']").click()
    time.sleep(1)
    random_product = random.randint(3, 8)
    #add random
    print(f"Add {random_product} to cart")
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
    
    #Check cart
    driver.find_element(By.XPATH, "//a[@href = '/cart']").click()
    time.sleep(1)
    cart_tr_elements = driver.find_elements(By.XPATH, "//tbody/tr")
    shipping_charge_element = cart_tr_elements[-2].find_elements(By.XPATH, ".//td")[-1]
    VAT_element = cart_tr_elements[-1].find_elements(By.XPATH, ".//td")[-1]
    total = float(shipping_charge_element.text[1:]) + float(VAT_element.text[1:])

    check = True
    for tr_element in cart_tr_elements[:-2]:
        td_element = tr_element.find_elements(By.XPATH, ".//td")
        p_in_cart = next((product_name for product_name in product_list.keys() if product_name == td_element[0].text), "")
        price = product_list[p_in_cart][0]
        quan = product_list[p_in_cart][1]
        sub_total = (price * quan)
        total += sub_total
         
        check_name = bool(p_in_cart)
        check_price = price == float(td_element[1].text[1:])
        check_quan = quan == float(td_element[2].text)
        check_sub_total = sub_total == float(td_element[3].text[1:])
        print(f'"{p_in_cart}": {check_name}')
        print(f"     price: {price} - {check_price}")
        print(f"     quantity: {quan} - {check_quan}")
        print(f"     sub_total: {price * quan} - {check_sub_total}", "\n")
        check = check and check_name and check_price and check_quan and check_sub_total
    total_text = driver.find_element(By.XPATH, "//td/h5/strong").text
    total_in_web = float(re.search(r'\d+', total_text).group())
    check_total = total == total_in_web
    print(f"Total: {total} - {check_total}")

    time.sleep(5)
    assert check and check_total

#Testcase 4 
def test_delete_product_in_cart(driver):
    #condition
    login(driver)
    add_random_product(driver)

    #main
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

    time.sleep(5)
    assert out_of_product

#Testcase 5
def test_use_coupon(driver):
    #condition
    login(driver)
    add_random_product(driver)

    #main
    driver.find_element(By.XPATH, "//a[@href = '/cart']").click()
    driver.find_element(By.ID, "exampleFormControlInput1").send_keys("ED60")
    driver.find_element(By.XPATH, "//tfoot/tr/td/button[text() = 'Apply']").click()
    time.sleep(1)

    total_text = driver.find_element(By.XPATH, "//td/h5/strong[contains(text(), 'Total')]").text
    total = float(re.search(r'\d+', total_text).group())
    discount_text = driver.find_element(By.XPATH, "//td/h5/strong[contains(text(), 'Discount')]").text
    discount = float(re.search(r'\d+', discount_text).group())
    total_discount_text = driver.find_element(By.XPATH, "//td/h3/strong").text
    total_discount = float(re.search(r'\d+', total_discount_text).group())
    
    cart_tr_elements = driver.find_elements(By.XPATH, "//tbody/tr")
    shipping_charge_element = cart_tr_elements[-2].find_elements(By.XPATH, ".//td")[-1]
    VAT_element = cart_tr_elements[-1].find_elements(By.XPATH, ".//td")[-1]
    total_no_fee = total - float(shipping_charge_element.text[1:]) - float(VAT_element.text[1:])

    check_discount = (total_no_fee * 0.6) == discount
    check_total_after_discount = (total - discount) == total_discount

    print(f"Check discount: {check_discount}")
    print(f"Check total after discount: {check_total_after_discount}")
    time.sleep(5)
    assert check_discount and check_total_after_discount

#pytest -s Test_cart.py
#5 Testcase