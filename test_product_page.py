import pytest
from stepikpython.pages.product_page import ProductPage

# Можете добавить сюда список URL для тестирования разных товаров
tested_urls = [
    "http://selenium1py.pythonanywhere.com/catalogue/the-shellcoders-handbook_209/?promo=newYear",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=newYear2019"
]

@pytest.mark.parametrize('url', tested_urls)
def test_guest_can_add_product_to_basket(browser, url):
    # 1. Открываем страницу товара
    page = ProductPage(browser, url)
    page.open()

    # 2. Получаем название и цену товара ДО добавления в корзину
    expected_product_name = page.get_product_name()
    expected_product_price = page.get_product_price()
    print(f"Testing product: {expected_product_name}, price: {expected_product_price}")

    # 3. Добавляем товар в корзину (внутри этого метода решается quiz)
    page.add_product_to_basket()

    # 4. Проверяем, что товар добавлен с правильным названием
    page.should_be_product_added_to_basket()

    # 5. Проверяем, что стоимость корзины совпадает с ценой товара
    page.should_be_basket_total_matches_price()

# Дополнительный тест для проверки работы с конкретным товаром
def test_guest_can_add_shellcoders_handbook_to_basket(browser):
    url = "http://selenium1py.pythonanywhere.com/catalogue/the-shellcoders-handbook_209/?promo=newYear"
    page = ProductPage(browser, url)
    page.open()
    page.add_product_to_basket()
    page.should_be_product_added_to_basket()
    page.should_be_basket_total_matches_price()

# ОТДЕЛЬНЫЙ тест для поиска бага с промо-акциями
@pytest.mark.parametrize('link', [
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer0",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer1",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer2",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer3",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer4",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer5",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer6",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer7",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer8",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer9"
])
def test_guest_can_add_product_to_basket_with_all_offers(browser, link):
    """
    Тест проверяет добавление товара в корзину для всех промо-предложений.
    Находит баг на одной из страниц.
    """
    page = ProductPage(browser, link)
    page.open()

    # Получаем название и цену товара
    expected_product_name = page.get_product_name()
    expected_product_price = page.get_product_price()
    print(f"\nTesting: {link}")
    print(f"Product: {expected_product_name}, Price: {expected_product_price}")

    # Добавляем товар в корзину
    page.add_product_to_basket()

    # Проверяем результаты (здесь будет падение на странице с багом)
    page.should_be_product_added_to_basket()
    page.should_be_basket_total_matches_price()