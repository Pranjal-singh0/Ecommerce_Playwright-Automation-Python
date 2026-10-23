import pytest
import logging
from utils.login_utils import load_credentials
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

logger = logging.getLogger(__name__)

@pytest.mark.smoke
def test_checkout_flow(page):
    creds = load_credentials("valid_user")
    logger.info("Loaded credentials for valid_user")

    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    logger.info("Navigating to login page and logging in")
    login_page.load()
    login_page.login(creds["username"], creds["password"])

    logger.info("Adding first item to cart")
    inventory_page.add_first_item_to_cart()

    logger.info("Opening cart to review added item")
    inventory_page.open_cart()

    logger.info("Initiating checkout")
    page.click("button#checkout")

    logger.info("Filling out checkout form")
    checkout_page.fill_checkout_info(creds["first_name"], creds["last_name"],str(creds["postal_code"]) )

    logger.info("Finishing checkout process")
    checkout_page.finish_order()

    success_msg = checkout_page.get_order_success_message()
    logger.info(f"Success message received: '{success_msg}'")
    assert "Thank you for your order" in success_msg
