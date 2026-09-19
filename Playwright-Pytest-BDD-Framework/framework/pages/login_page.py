from playwright.sync_api import expect


class LoginPage:
    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url

    def open(self):
        self.page.goto(self.base_url + "/login")

    def sign_in(self, username, password):
        self.page.get_by_label("Username", exact=True).fill(username)
        self.page.get_by_label("Password", exact=True).fill(password)
        self.page.get_by_role("button", name="Sign in", exact=True).click()

    def assert_invalid(self):
        expect(self.page.get_by_role("alert")).to_have_text("invalid_credentials")
