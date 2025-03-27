import pytest
from playwright.sync_api import expect

@pytest.mark.parametrize("username,password", [("standard_user", "secret_sauce")])
def test_login(page, username, password):
    page.goto("https://www.saucedemo.com/")
    page.locator("#user-name").fill(username)
    page.locator("#password").fill(password)
    page.locator("#login-button").click()
    expect(page.locator(".inventory_list")).to_be_visible()
