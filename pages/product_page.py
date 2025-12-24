from .base_page import BasePage
from .locators import ProductPageLocators


class ProductPage(BasePage):
    def add_product_to_basket(self):
        """Нажимаем кнопку добавления в корзину и решаем quiz"""
        add_button = self.browser.find_element(*ProductPageLocators.ADD_TO_BASKET_BUTTON)
        add_button.click()
        self.solve_quiz_and_get_code()

    def get_product_name(self):
        """Получаем название товара со страницы"""
        return self.browser.find_element(*ProductPageLocators.PRODUCT_NAME).text

    def get_product_price(self):
        """Получаем цену товара со страницы"""
        return self.browser.find_element(*ProductPageLocators.PRODUCT_PRICE).text

    def should_be_product_added_to_basket(self):
        """Проверяем, что товар добавлен в корзину с правильным названием"""
        product_name = self.get_product_name()
        success_message = self.browser.find_element(*ProductPageLocators.SUCCESS_MESSAGE).text
        assert product_name == success_message, \
            f"Product name in message is wrong. Expected: '{product_name}', got: '{success_message}'"

    def should_be_basket_total_matches_price(self):
        """Проверяем, что стоимость корзины совпадает с ценой товара"""
        product_price = self.get_product_price()
        basket_total = self.browser.find_element(*ProductPageLocators.BASKET_TOTAL_MESSAGE).text
        assert product_price == basket_total, \
            f"Basket total doesn't match product price. Expected: '{product_price}', got: '{basket_total}'"