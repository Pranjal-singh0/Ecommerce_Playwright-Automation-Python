# tests/login/test_login_valid.py

import pytest
from pages.inventory_page import InventoryPage
from utils.login_utils import load_credentials
from pages.login_page import LoginPage


def test_login_valid_user(page):
    creds = load_credentials("valid_user")

    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.load()
    login_page.login(creds["username"], creds["password"])

    assert inventory_page.item_count() > 0



@pytest.mark.parametrize("username,password", [("invalid_user", "wrong_pass")])
def test_login_invalid_user(page, username, password):
    login_page = LoginPage(page)

    login_page.load()
    login_page.login(username, password)

    # Assert error message is visible
    assert login_page.error_message.is_visible()
    assert "Username and password do not match" in login_page.error_message.text_content()