from playwright.sync_api import expect


class ShopPage:
    def __init__(self, page):
        self.page = page

    def assert_ready(self):
        expect(
            self.page.get_by_role("heading", name="Shop", exact=True)
        ).to_be_visible()

    def place_order(self, sku, quantity):
        self.page.get_by_label("Product", exact=True).select_option(sku)
        self.page.get_by_label("Quantity", exact=True).fill(str(quantity))
        self.page.get_by_role("button", name="Place order", exact=True).click()
        expect(
            self.page.get_by_role("heading", name="Order confirmation")
        ).to_be_visible()

    def assert_total(self, total):
        expect(self.page.get_by_test_id("order-total")).to_have_text(total)

    def order_id(self):
        return self.page.get_by_test_id("order-id").inner_text()

    def sign_out(self):
        self.page.get_by_role("button", name="Sign out", exact=True).click()
        expect(
            self.page.get_by_role("button", name="Sign in", exact=True)
        ).to_be_visible()
