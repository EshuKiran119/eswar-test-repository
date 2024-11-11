from selenium import webdriver
from selenium.webdriver.common.by import By

def find_total_articles_by_languages(driver, languages):
    total_articles = 0

    for language in languages:
        # Locate the row in the table for the specified language
        language_xpath = f"//table[contains(@class, 'wikitable')]/tbody/tr[td[2]//a[contains(text(), '{language}')]]/td[4]"
        element = driver.find_element(By.XPATH, language_xpath)
        article_count = element.text.replace(",", "")

        # Convert to integer and add to total
        total_articles += int(article_count)
        print(f"{language}: {article_count} articles")

    return total_articles

if __name__ == "__main__":
    # Initialize the WebDriver
    driver = webdriver.Chrome()
    driver.get("https://meta.wikimedia.org/wiki/List_of_Wikipedias/Table")
    driver.maximize_window()

    languages = ["English", "German"]
    total = find_total_articles_by_languages(driver, languages)
    
    print(f"Total articles for {', '.join(languages)}: {total}")
    driver.quit()
