import os 
import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AmazonScraper:
    def __init__(self, driver_path, page_limit):
        self.driver_path = driver_path
        self.page_limit = page_limit
        self.driver = None

    def __enter__(self):
        self.driver = webdriver.Chrome(self.driver_path, options=self.chrome_options)
        self.driver.get("https://www.amazon.com/s?i=computers-intl-ship&bbn=16225007011&rh=n%3A16225007011%2Cp_36%3A1253503011&dc&fs=true&qid=1645954406&ref=sr_ex_n_1")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.quit_driver()

    def quit_driver(self):
        if self.driver:
            self.driver.quit()

    def scrape(self):
        with open("data.json", "w") as f:
            json.dump([], f)

    def run(self):
        while not self.page_limit:
            try:
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@data-component-type='s-search-result']"))
                )
                elem_list = self.driver.find_element(
                    By.XPATH, "//div[@class='s-main-slot s-result-list s-search-results sg-row']"
                )
                items = elem_list.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")
                for item in items:
                    time.sleep(1)
                    item_title = item.find_element(By.TAG_NAME, "h2").text
                    item_price = "not found"
                    item_image = "no image found"
                    item_url = item.find_element(By.CLASS_NAME, "a-link-normal").get_attribute("href")
                    try:
                        item_price = item.find_element(By.CLASS_NAME, "a-price").text.replace("\n", ".").replace("$", "")
                        item_price = float(item_price)
                    except:
                        pass
                    try:
                        item_image = item.find_element(By.CSS_SELECTOR, ".s-image").get_attribute("src")
                    except:
                        pass
                    print("Title:" + item_title)
                    print("Price:", item_price)
                    print("Image:" + item_image)
                    print("Url:" + item_url + "\n")
                    self.data.append(
                        {"Title": item_title, "Price": item_price, "Image": item_image, "Url": item_url}
                    )
                next_btn = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "s-pagination-next"))
                )
                next_class = next_btn.get_attribute("aria-label")
                if "page 4" in next_class:
                    self.page_limit = True
                else:
                    self.driver.find_element(By.CLASS_NAME, "s-pagination-next").click()
            except Exception as e:
                print(e, "Main Error")
                self.page_limit = True

    def save_to_file(self, filename):
        with open(filename, "w") as f:
            json.dump(self.data, f, indent=4)

    def __del__(self):
        self.driver.quit()


if __name__ == "__main__":
    url = "https://www.amazon.com/s?i=computers-intl-ship&bbn=16225007011&rh=n%3A16225007011%2Cp_36%3A1253503011&dc&fs=true&qid=1645954406&ref=sr_ex_n_1"
    path = "/Users/mac/my_workshops/scraping_bs4/fullselenium/chromedriver"
    scraper = AmazonScraper(url=url, path=path)
    scraper.run()
    scraper.save_to_file("data2.json")
