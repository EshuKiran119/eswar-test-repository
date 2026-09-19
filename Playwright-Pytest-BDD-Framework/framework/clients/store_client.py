import requests


class StoreClient:
    """One session per test, explicit timeouts, no mutation retries."""

    def __init__(self, settings):
        self.settings = settings
        self.session = requests.Session()
        self.token = None
        self.orders = set()

    def request(self, method, path, **kwargs):
        return self.session.request(
            method,
            self.settings.base_url + path,
            timeout=self.settings.timeout,
            **kwargs
        )

    def login(self, name, password):
        r = self.request(
            "POST", "/api/login", json={"username": name, "password": password}
        )
        if r.status_code == 200:
            self.token = r.json()["token"]
            self.session.headers["Authorization"] = "Bearer " + self.token
        return r

    def create_order(self, sku, quantity):
        r = self.request("POST", "/api/orders", json={"sku": sku, "quantity": quantity})
        if r.status_code == 201:
            self.orders.add(r.json()["id"])
        return r

    def logout(self):
        try:
            return self.request("POST", "/api/logout", json={})
        finally:
            self.token = None
            self.session.headers.pop("Authorization", None)

    def close(self):
        try:
            if self.token:
                for oid in self.orders:
                    self.request("DELETE", "/api/orders/" + oid)
                self.logout()
        finally:
            self.session.close()
