from pytest_bdd import given, when, then, parsers
from playwright.sync_api import expect
from framework.pages.login_page import LoginPage
from framework.pages.shop_page import ShopPage


@given("the login page is open", target_fixture="login_page")
def login(page, settings):
    view = LoginPage(page, settings.base_url)
    view.open()
    return view


@given("the customer is signed in through the browser", target_fixture="shop_page")
def signed(page, settings, credentials):
    view = LoginPage(page, settings.base_url)
    view.open()
    view.sign_in(*credentials)
    shop = ShopPage(page)
    shop.assert_ready()
    return shop


@when(
    parsers.parse('the customer buys {quantity:d} units of "{sku}" through the browser')
)
def buy(shop_page, state, sku, quantity):
    shop_page.place_order(sku, quantity)
    state.update(sku=sku, quantity=quantity)


@then(parsers.parse('the browser displays an order total of "{total}"'))
def total(shop_page, total):
    shop_page.assert_total(total)


@then("the browser order matches the stored API order")
def mapping(shop_page, api, credentials, state):
    assert api.login(*credentials).status_code == 200
    oid = shop_page.order_id()
    api.orders.add(oid)
    response = api.request("GET", "/api/orders/" + oid)
    assert response.status_code == 200
    order = response.json()
    assert order["sku"] == state["sku"]
    assert order["quantity"] == state["quantity"]
    assert order["total_cents"] == 2500
    assert order["owner"] == credentials[0]
    shop_page.sign_out()
    api.orders.discard(oid)


@when("an incorrect password is submitted through the browser")
def invalid(login_page, credentials):
    login_page.sign_in(credentials[0], "incorrect-demo-password")


@then("the browser shows an invalid credentials message")
def rejected(login_page):
    login_page.assert_invalid()


@when("the customer signs out through the browser")
def logout(shop_page):
    shop_page.sign_out()


@then("the login form is visible")
def visible(page):
    expect(page.get_by_role("button", name="Sign in", exact=True)).to_be_visible()
