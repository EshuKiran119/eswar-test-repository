import pytest

pytestmark = [pytest.mark.api, pytest.mark.regression]


@pytest.mark.parametrize("quantity", [True, "2", None, 1.5])
def test_quantity_requires_integer(api, credentials, quantity):
    assert api.login(*credentials).status_code == 200
    r = api.create_order("notebook", quantity)
    assert r.status_code == 400
    assert r.json()["error"] == "invalid_quantity"


def test_anonymous_catalog_is_rejected(api):
    assert api.request("GET", "/api/products").status_code == 401


def test_unknown_product_is_rejected(api, credentials):
    assert api.login(*credentials).status_code == 200
    r = api.create_order("missing-sku", 1)
    assert r.status_code == 400
    assert r.json()["error"] == "unknown_product"


def test_deleted_order_is_not_found(api, credentials):
    assert api.login(*credentials).status_code == 200
    r = api.create_order("mug", 1)
    assert r.status_code == 201
    oid = r.json()["id"]
    assert api.request("DELETE", "/api/orders/" + oid).status_code == 204
    api.orders.remove(oid)
    assert api.request("GET", "/api/orders/" + oid).status_code == 404
