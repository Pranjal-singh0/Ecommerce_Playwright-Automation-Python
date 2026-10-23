# tests/cart/test_add_to_cart.py

from utils.login_utils import load_credentials
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

def test_add_item_to_cart(page):
    creds = load_credentials("valid_user")

    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    login_page.load()
    login_page.login(creds["username"], creds["password"])

    first_item_name = inventory_page.get_all_item_names()[0]
    inventory_page.add_first_item_to_cart()
    inventory_page.open_cart()

    cart_items = cart_page.get_cart_item_names()

    assert first_item_name in cart_items
    assert cart_page.cart_count() == 1
