from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
import json
import time

web = 'https://www.adamchoi.co.uk/overs/detailed'
path = '/Users/mac/my_workshops/SELENIUM/footTables/chromedriver'
driver = webdriver.Chrome(path)
driver.get(web)


all_matches_button = driver.find_element_by_xpath("//label[@analytics-event='All matches']").click()
data = []

select = Select(driver.find_element_by_id('country'))
for option in select.options:
    
    select.select_by_visible_text(option.text)
    time.sleep(2)
    
    date_element = driver.find_elements_by_xpath("//td[1]")
    time.sleep(2)
    team1_element = driver.find_elements_by_xpath("//td[2]")
    time.sleep(2)
    score_element = driver.find_elements_by_xpath("//td[3]")
    time.sleep(2)
    team2_element = driver.find_elements_by_xpath("//td[4]")
    time.sleep(2)
    date = [date.text for date in date_element]
    team1 = [team1.text for team1 in team1_element]
    score = [score.text for score in score_element] 
    team2 = [team2.text for team2 in team2_element]
    time.sleep(2)
    for i in range(len(date)):
        
        data.append({
            'pays': option.text,
            'date':date[i],
            'team1':team1[i],
            'score':score[i],
            'team2':team2[i]
        })
    print(data)
# Exportation des données au format JSON
with open("/Users/mac/my_workshops/SELENIUM/footTables/resultats.json", "w") as f:
    json.dump(data, f)


df = pd.DataFrame.from_dict(data)
df.to_csv('/Users/mac/my_workshops/SELENIUM/footTables/data.csv', index=False)        
        
        
    
     
    

time.sleep(4)

driver.quit()