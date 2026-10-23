# pages/inventory_page.py

from pages.base_page import BasePage

class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.inventory_items = page.locator(".inventory_item")

    def item_count(self):
        return self.inventory_items.count()

    def get_all_item_names(self):
        return self.page.locator(".inventory_item_name").all_text_contents()

    def add_first_item_to_cart(self):
        self.page.locator("button.btn_inventory").first.click()

    def open_cart(self):
        self.page.click("a.shopping_cart_link")
    
    def sort_items(self, option_text):
        # e.g. "Price (low to high)", "Name (Z to A)"
        self.page.select_option("select.product_sort_container", label=option_text)

    def add_item_by_name(self, item_name):
        locator = self.page.locator(f"text={item_name} >> xpath=../..//button[contains(@class, 'btn_inventory')]")
        locator.click()

    def remove_item_by_name(self, item_name):
        locator = self.page.locator(f"text={item_name} >> xpath=../..//button[contains(text(), 'Remove')]")
        locator.click()

