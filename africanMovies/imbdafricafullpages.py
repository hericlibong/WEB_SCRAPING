from bs4 import BeautifulSoup
import requests
import json
import  pandas as pd

# Selection of african movies on imdb website

def extract_data(container):
        title = container.find('h3', class_='lister-item-header').find('a').get_text()
        year = container.find('span', class_='lister-item-year text-muted unbold').get_text()
        try:
            certif = container.find('span', class_='certificate').get_text()
        except:
            certif = 'None'
        try:
            time = container.find('span', class_='runtime').get_text()
        except:
            time = 'None'
        try:
            genre = container.find('span', class_='genre').get_text(strip=True)
        except :
            genre  = 'None'
        star = container.find('span', class_='ipl-rating-star__rating').get_text()
            #penser à  mettre  une condition  sur les métas
        try:
            meta= container.find('div', class_='inline-block ratings-metascore').find('span').get_text(strip=True)
        except:
            meta = 'None'        
        resume = container.find_all('p')[1].get_text(strip=True)
        director = container.find_all('p')[2].find('a').get_text()
        acteurs = [item.get_text() for item in container.find_all('p')[2].find_all('a')]
        #vote = container.find_all(attrs={"name": "nv"}).get_text()
        try:
            vote = [item.get_text() for item in container.find_all('span',attrs={"name":"nv"})][0]
        except:
            vote= 'None'
        try:
            gross= [item.get_text() for item in container.find_all('span', attrs={"name":"nv"})][1]
        except:
            gross= 'None'
        data = {'Title':title, 
                'Year':year, 
                'Certification': certif,
                'Time':time,  
                'Genre':genre, 
                'Star':star,
                'Meta':meta,
                'Resume':resume,
                'Director':director,
                'Actors':acteurs,
                'Vote': vote,
                'Gross':gross
                } 
        return data
    
    
    
def get_quote(pageurl):
    page  = requests.get(pageurl)
    parsedPage = BeautifulSoup(page.content, 'lxml') 
    containers = parsedPage.find_all('div', class_='lister-item-content')
    if len(containers)>0:
        liste_containers = [extract_data(cont) for cont in containers]
        return liste_containers
    else:
        return  None
data = get_quote('https://www.imdb.com/list/ls051534056/?st_dt=&mode=detail&page=1&sort=list_order,asc')

for i in range(2, 4):
    print(i)
    page_url = f'https://www.imdb.com/list/ls051534056/?st_dt=&mode=detail&page={i}&sort=list_order,asc'
    current_page = get_quote(page_url)
    if  current_page is not None:
        data  = data + current_page
    else:
        break

data_pd = pd.DataFrame.from_dict(data)
print(data_pd)


data_pd.to_csv('/Users/mac/my_workshops/SCRAPING_BS4/africanMovies/moviesFullpage.csv')
#data_pd.to_json('/Users/mac/lessons/UDEMY-SCRAPING-ANDRADE/africanMovies/movies2.json')
        
        
    
    
    

    
    