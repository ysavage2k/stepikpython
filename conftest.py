import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption(
        '--language',
        action='store',
        default='en',
        help='Choose browser language'
    )


@pytest.fixture(scope="function")
def browser(request):
    # Получаем язык из командной строки
    user_language = request.config.getoption("language")

    # Настраиваем Chrome
    options = Options()
    options.add_experimental_option('prefs', {
        'intl.accept_languages': user_language
    })

    # Инициализируем браузер
    print(f"\nStart browser with language: {user_language}")
    browser = webdriver.Chrome(options=options)

    # Передаем браузер тесту
    yield browser

    # Закрываем браузер после теста
    print("\nQuit browser")
    browser.quit()