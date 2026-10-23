# pages/cart_page.py

from pages.base_page import BasePage

class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.cart_items = page.locator(".cart_item")
        self.item_names = page.locator(".inventory_item_name")

    def get_cart_item_names(self):
        return self.item_names.all_text_contents()

    def cart_count(self):
        return self.cart_items.count()
