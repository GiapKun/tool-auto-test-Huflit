from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Thiết lập Chrome options (nếu cần)
chrome_options = Options()
chrome_options.add_argument('--headless')  
chrome_options.add_argument('--disable-gpu')

# Khởi tạo trình điều khiển (driver) một lần
driver = webdriver.Chrome(options=chrome_options)

def get_data(driver, url, number_a, number_b, operation_type, prototype):
    result = {}  # Khởi tạo biến result trước
    wait = WebDriverWait(driver, 10)  # Tối đa chờ 10 giây

    try:
        # Mở trang web
        driver.get(url)

        # Nhập số đầu tiên
        input1 = wait.until(EC.presence_of_element_located((By.ID, 'number1Field')))
        input1.clear()
        input1.send_keys(str(number_a))  # Chuyển số thành chuỗi trước khi nhập

        # Nhập số thứ hai
        input2 = driver.find_element(By.ID, 'number2Field')
        input2.clear()
        input2.send_keys(str(number_b))  # Chuyển số thành chuỗi trước khi nhập

        # Chọn phép tính
        operation_dropdown = driver.find_element(By.ID, 'selectOperationDropdown')
        for option in operation_dropdown.find_elements(By.TAG_NAME, 'option'):
            if option.text == operation_type:
                option.click()
                break

        # Chọn giá trị cho 'prototype'
        prototype_dropdown = driver.find_element(By.ID, 'selectBuild')
        for option in prototype_dropdown.find_elements(By.TAG_NAME, 'option'):
            if option.text == str(prototype):
                option.click()
                break

        # Nhấn nút tính toán
        button = driver.find_element(By.ID, 'calculateButton')
        button.click()  # Nhấn vào nút

        # Chờ kết quả không làm tròn hiển thị
        output_without_integer = wait.until(EC.presence_of_element_located((By.ID, 'numberAnswerField')))
        result['without_integer'] = output_without_integer.get_attribute('value')

        # # Tích vào checkbox "integer" và lấy kết quả đã làm tròn
        # integer_checkbox = driver.find_element(By.ID, 'integerSelect')
        # integer_checkbox.click()

        # # Chờ kết quả làm tròn cập nhật
        # output_with_integer = wait.until(EC.presence_of_element_located((By.ID, 'numberAnswerField')))
        # result['with_integer'] = output_with_integer.get_attribute('value')

    except Exception as e:
        print(f"Error occurred: {e}")
        # result['error'] = str(e)

    return result

# Ví dụ sử dụng hàm
results = []
url = 'https://testsheepnz.github.io/BasicCalculator.html'
# Quantity of test cases n = 5
for i in range(5):
    a = random.randint(-500, 500)
    b = random.randint(-500, 500)
    result = get_data(driver, url, number_a=a, number_b=b, operation_type='Concatenate', prototype=6)
    result['a'] = a
    result['b'] = b
    results.append(result)

print(results)

# Đóng trình điều khiển khi hoàn thành
driver.quit()
