import os 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

with open("data.json", "w") as f:
    json.dump([], f)

def write_json(new_data, filename='data.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data.append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)


Path = '/Users/mac/my_workshops/scraping_bs4/fullselenium/chromedriver'
driver = webdriver.Chrome(Path, options=chrome_options)
driver.get("https://www.amazon.com/s?i=computers-intl-ship&bbn=16225007011&rh=n%3A16225007011%2Cp_36%3A1253503011&dc&fs=true&qid=1645954406&ref=sr_ex_n_1")

page_limit = False

while not page_limit:
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@data-component-type='s-search-result']")))
        
        elem_list = driver.find_element(By.XPATH, "//div[@class='s-main-slot s-result-list s-search-results sg-row']")
    
        items  = elem_list.find_elements(By.XPATH,"//div[@data-component-type='s-search-result']")

        for item  in items:
            time.sleep(1)
            item_title = item.find_element(By.TAG_NAME, 'h2').text
            item_price = "not found"
            item_image = "no image found"
            item_url = item.find_element(By.CLASS_NAME, "a-link-normal").get_attribute("href")
            try :
                item_price = item.find_element(By.CLASS_NAME, "a-price").text.replace("\n", ".").replace("$", "")
                item_price = float(item_price)
            except :
                pass 
                
            try :
                item_image = item.find_element(By.CSS_SELECTOR, ".s-image").get_attribute("src")
            except :
                pass

    
            print("Title:" + item_title)
            print("Price:" ,item_price)
            print("Image:" +item_image)
            print("Url:" +item_url + "\n")
            
            
            write_json({
                "Title": item_title,
                "Price":  item_price,
                "Image": item_image,
                "Url": item_url 
                })
        
        
        next_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CLASS_NAME, 's-pagination-next'))) 
        next_class = next_btn.get_attribute('aria-label') 
        
        #Limited to 3 pages. 
        # for more page set the number of the condition.  
        # if you want all page  change the name of the attribute of next_class line with 'class'
        # set the condition to "disabled"
        if  'page 4' in next_class:
            page_limit = True
        else :
            driver.find_element(By.CLASS_NAME, 's-pagination-next').click() 
        
    except Exception as e:
        print(e, "Main Error")
        page_limit = True    
     
    
        
   
