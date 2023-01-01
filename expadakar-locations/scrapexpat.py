from bs4  import BeautifulSoup
import requests
import json
import pandas as pd

page = requests.get('https://www.expat-dakar.com/appartements-a-louer')

if page.status_code==200:
    parsedPage = BeautifulSoup(page.content, 'lxml')
    container  = parsedPage.find_all('div',  class_='listings-cards__list-item')
    
    def extract_data(container):
        
    
        apt_name = container.find('div', class_= 'listing-card__header__title').get_text(strip=True)
        rooms = container.find('div', class_='listing-card__header__tags').find_all('span')[0].get_text()
        try:
            superficie = container.find('div', class_='listing-card__header__tags').find_all('span')[1].get_text()
        except :
            superficie='None'
        image_url = container.find('img', class_='listing-card__image__resource vh-img')['src']
        location = container.find('div', class_='listing-card__header__location').get_text(strip=True)
        date = container.find('div', class_='listing-card__header__date').get_text(strip=True)
        prix = container.find('span', class_='listing-card__price__value 1').get_text(strip=True).split('\u202f')
    
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
    
    liste_container = []
    for cont in container:
        liste_container.append(extract_data(cont))
    print(liste_container)
    # with open('/Users/mac/my_workshops/SCRAPING_BS4/expadakar-locations/aptlocations.json', 'w') as f:
    #     json.dump(liste_container, f)
    df = pd.DataFrame.from_dict(liste_container)
    print(df)
    df.to_csv('/Users/mac/my_workshops/SCRAPING_BS4/expadakar-locations/aptpage1.csv')
    