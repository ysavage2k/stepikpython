import math
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def calc(x):
    """Вычисление математической функции"""
    return str(math.log(abs(12 * math.sin(int(x)))))


try:
    browser = webdriver.Chrome()
    browser.get("http://suninjuly.github.io/explicit_wait2.html")

    # 1. Ждем, когда цена дома уменьшится до $100 (ждем не менее 12 секунд)
    price_element = browser.find_element(By.ID, "price")

    # Используем явное ожидание
    wait = WebDriverWait(browser, 15)  # Ожидание до 15 секунд

    # Ждем, пока в элементе с id="price" появится текст "$100"
    wait.until(
        EC.text_to_be_present_in_element((By.ID, "price"), "$100")
    )

    # 2. Нажимаем на кнопку "Book"
    book_button = browser.find_element(By.ID, "book")
    book_button.click()

    # 3. Решаем математическую задачу
    # Получаем значение x
    x_element = browser.find_element(By.ID, "input_value")
    x = x_element.text
    y = calc(x)

    # Вводим ответ
    answer_input = browser.find_element(By.ID, "answer")
    answer_input.send_keys(y)

    # Нажимаем кнопку Submit
    submit_button = browser.find_element(By.ID, "solve")
    submit_button.click()

    # 4. Получаем число из alert
    time.sleep(1)
    alert = browser.switch_to.alert
    result_text = alert.text

    # Извлекаем число из текста
    import re

    numbers = re.findall(r"\d+\.\d+|\d+", result_text)
    if numbers:
        answer = numbers[-1]
        print(f"Число для ответа: {answer}")
    else:
        print(f"Весь текст alert: {result_text}")

    alert.accept()
#test com
finally:
    time.sleep(5)
    browser.quit()