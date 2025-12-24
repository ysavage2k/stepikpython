import math
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def compute_answer():
    """Вычисляет правильный ответ по заданной формуле: log(текущее время в секундах)."""
    return str(math.log(int(time.time())))


@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.mark.parametrize('url', [
    "https://stepik.org/lesson/236895/step/1",
    "https://stepik.org/lesson/236896/step/1",
    "https://stepik.org/lesson/236897/step/1",
    "https://stepik.org/lesson/236898/step/1",
    "https://stepik.org/lesson/236899/step/1",
    "https://stepik.org/lesson/236903/step/1",
    "https://stepik.org/lesson/236904/step/1",
    "https://stepik.org/lesson/236905/step/1"
])
def test_stepik_feedback(browser, url):
    print(f"\n=== Тестирую URL: {url} ===")

    # 1. Открыть страницу
    browser.get(url)

    # 2. Авторизация
    login = "hlvqwe@gmail.com"
    password = "kbR)3cuZiAnxYM+"

    print("Требуется авторизация")

    # Находим и нажимаем кнопку "Войти"
    try:
        login_button = browser.find_element(By.CSS_SELECTOR, "a.navbar__auth_login")
    except:
        login_button = browser.find_element(By.XPATH, "//a[contains(text(), 'Войти')]")

    print("Найдена кнопка входа, нажимаю...")
    login_button.click()

    # Ждём форму и заполняем
    email_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "id_login_email"))
    )
    print("Форма логина загружена")

    email_input.send_keys(login)
    password_input = browser.find_element(By.ID, "id_login_password")
    password_input.send_keys(password)

    submit_button = browser.find_element(By.CSS_SELECTOR, "button.sign-form__btn")
    submit_button.click()

    # Ждём завершения авторизации
    WebDriverWait(browser, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.modal-dialog"))
    )
    print("Авторизация успешна")

    # 3. Ввести ответ
    answer = compute_answer()
    print(f"Вычисленный ответ: {answer}")

    # Находим поле для ответа
    textarea = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.ember-text-area"))
    )
    print("Текстовое поле найдено")

    textarea.clear()
    textarea.send_keys(answer)
    print("Ответ введён")

    # 4. Нажать "Отправить"
    submit_button = browser.find_element(By.CSS_SELECTOR, "button.submit-submission")
    submit_button.click()
    print("Кнопка 'Отправить' нажата")

    # 5. Ждём ОПЦИОНАЛЬНЫЙ ФИДБЕК (чёрное поле с текстом)
    # Даём время на обработку ответа
    time.sleep(3)

    # Ищем именно элемент с фидбеком
    try:
        # Сначала ищем по специфичным классам
        feedback_element = browser.find_element(By.CSS_SELECTOR,
                                                "div.attempt-message_correct, "
                                                "div.attempt__message.attempt__message_correct, "
                                                "div.smart-hints__feedback")
    except:
        try:
            # Ищем по тексту "Correct" или "Правильно"
            feedback_element = browser.find_element(By.XPATH,
                                                    "//div[contains(text(), 'Correct') or contains(text(), 'Правильно')]")
        except:
            try:
                # Ищем любой небольшой элемент с фидбеком (не весь блок страницы)
                all_divs = browser.find_elements(By.CSS_SELECTOR, "div")
                for div in all_divs:
                    text = div.text.strip()
                    if text and len(text) < 100:  # Ищем короткий текст
                        print(f"Найден короткий текст: '{text}'")
                        feedback_element = div
                        break
                else:
                    raise Exception("Не найден элемент с фидбеком")
            except:
                # Если всё ещё не нашли, используем последний резерв
                feedback_element = browser.find_element(By.CSS_SELECTOR, "div.smart-hints")

    # 6. Проверяем текст
    feedback_text = feedback_element.text.strip()
    print(f"Текст фидбека: '{feedback_text}'")

    # Удаляем лишние пробелы и переносы строк
    clean_feedback = ' '.join(feedback_text.split())

    expected_text = "Correct!"

    # Сравниваем
    if clean_feedback != expected_text:
        print(f"=== ФРАГМЕНТ ПОСЛАНИЯ НАЙДЕН: '{clean_feedback}' ===")
        # Сохраняем в файл
        with open("message.txt", "a", encoding="utf-8") as f:
            f.write(f"{url}\n{clean_feedback}\n\n")

    # Тест падает, если не "Correct!"
    assert clean_feedback == expected_text, \
        f'Ожидался текст "{expected_text}", но получен "{clean_feedback}". ' \
        f'URL: {url}'

    print("✓ Тест пройден")


if __name__ == "__main__":
    # Очищаем файл с сообщениями
    open("message.txt", "w").close()
    pytest.main(["-v", "-s", __file__])