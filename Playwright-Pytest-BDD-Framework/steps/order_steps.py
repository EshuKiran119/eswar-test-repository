from pytest_bdd import when, then, parsers
from framework.clients.store_client import StoreClient


@when(parsers.parse('the customer orders {quantity:d} units of "{sku}"'))
def create(api, state, quantity, sku):
    state["response"] = api.create_order(sku, quantity)


@then(
    parsers.parse(
        'the stored order has sku "{sku}", quantity {quantity:d} and total {total:d} cents'
    )
)
def mapping(api, state, credentials, sku, quantity, total):
    created = state["response"].json()
    read = api.request("GET", "/api/orders/" + created["id"])
    assert read.status_code == 200
    stored = read.json()
    assert stored == created
    assert stored["sku"] == sku
    assert stored["quantity"] == quantity
    assert stored["total_cents"] == total
    assert stored["unit_price_cents"] * quantity == total
    assert stored["owner"] == credentials[0]
    assert stored["status"] == "created"


@when("a different customer requests that order")
def other_user(state, settings, credentials):
    oid = state["response"].json()["id"]
    other = StoreClient(settings)
    i = int(credentials[0].removeprefix("sample")) % 20 + 1
    try:
        assert other.login(f"sample{i:02}", f"DemoOnly{i:02}!").status_code == 200
        state["response"] = other.request("GET", "/api/orders/" + oid)
    finally:
        other.close()
