from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
 
 
class Assignment:
    driver = None
 
    @staticmethod
    def res1():
        n = int(input("Enter the number of countries: "))
        Assignment.driver = webdriver.Chrome()
        Assignment.driver.get("https://meta.wikimedia.org/wiki/List_of_Wikipedias/Table")
        Assignment.driver.maximize_window()
        
        countries = []
        for i in range(n):
            country = input(f"Enter country {i + 1}: ")
            countries.append(country)
 
        Assignment.find_total_articles_by_languages(countries)
        Assignment.driver.quit()
 
    @staticmethod
    def find_total_articles_by_languages(countries):
        total_sum = 0
        wait = WebDriverWait(Assignment.driver, 10)
 
        for country in countries:
            try:
                # Locate the row containing the specified country name
                row = wait.until(EC.presence_of_element_located(
                    (By.XPATH, f"//table[contains(@class, 'sortable')]/tbody/tr[td[contains(., '{country}')]]")
                ))
 
                # Find the articles count in the 5th column of the identified row
                articles = row.find_element(By.XPATH, "./td[5]").text
                print(f"Articles for {country}: {articles}")
 
                # Clean up the article count (remove commas) and add to total sum
                article_count = int(articles.replace(',', ''))
                total_sum += article_count
 
            except (NoSuchElementException, TimeoutException):
                print(f"Could not find data for {country}")
 
        print(f"Sum of articles for the entered countries: {total_sum}")
 
 
if __name__ == "__main__":
    Assignment.res1()