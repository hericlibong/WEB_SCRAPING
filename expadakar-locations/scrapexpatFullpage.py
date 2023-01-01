from bs4  import BeautifulSoup
import requests
import json
import pandas as pd


    
def extract_data(container):
        
    
    apt_name = container.find('div', class_= 'listing-card__header__title').get_text(strip=True)
    try:
        rooms = container.find('div', class_='listing-card__header__tags').find_all('span')[0].get_text()
    except:
        rooms = None
    try:
        superficie = container.find('div', class_='listing-card__header__tags').find_all('span')[1].get_text()
    except :
        superficie='None'
    image_url = container.find('img', class_='listing-card__image__resource vh-img')['src']
    location = container.find('div', class_='listing-card__header__location').get_text(strip=True).split('\n')
    date = container.find('div', class_='listing-card__header__date').get_text(strip=True)
    try:
        prix = container.find('span', class_='listing-card__price__value 1').get_text(strip=True).split('\u202f')
    except :
        prix = 'None'
    
    data = {
        'Apt':apt_name,
        'Rooms':rooms,
        'Surface':superficie,
        'Picture_Url':image_url,
        'Location':location,
        'Date':date,
        'Price':prix        
        }
    return data

def get_urls(pageurl):
    page = requests.get(pageurl)
    parsedPage = BeautifulSoup(page.content, 'lxml')
    container = parsedPage.find_all('div',  class_='listings-cards__list-item')
    if len(container)<=11:
        liste_container = [extract_data(cont) for cont in container]
        return liste_container
    else:
        return None
data = get_urls('https://www.expat-dakar.com/appartements-a-louer')

for i in range(2, 126):
    print(i)
    page_url = f'https://www.expat-dakar.com/appartements-a-louer?page={i}'
    current_page = get_urls(page_url)
    if current_page is not None:
        data= data + current_page
    else :
        break
data_pd = pd.DataFrame.from_dict(data)
print(data_pd)
data_pd.to_csv('/Users/mac/my_workshops/SCRAPING_BS4/expadakar-locations/expatapart.csv')
        
    
    
    
   
  
    # df = pd.DataFrame.from_dict(liste_container)
    # print(df)
    # df.to_csv('/Users/mac/my_workshops/SCRAPING_BS4/expadakar-locations/aptfulldata.csv')
    