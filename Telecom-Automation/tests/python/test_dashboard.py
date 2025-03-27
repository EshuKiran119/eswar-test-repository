import unittest
from selenium import webdriver
from pages.login_page import LoginPage

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_valid_login(self):
        login_page = LoginPage(self.driver)
        login_page.login("admin", "admin")
        self.assertIn("overview.htm", self.driver.current_url)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
