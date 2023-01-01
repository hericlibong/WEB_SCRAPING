from bs4 import BeautifulSoup
import requests
import json
import pandas as pd


page = requests.get('https://www.imdb.com/list/ls051534056/?st_dt=&mode=detail&page=1&sort=list_order,asc')


if  page.status_code==200:
    parsedPage = BeautifulSoup(page.content, 'lxml')
    containers = parsedPage.find_all('div', class_='lister-item-content')


    def extract_data(container):
        title = container.find('h3', class_='lister-item-header').find('a').get_text()
        year = container.find('span', class_='lister-item-year text-muted unbold').get_text()
        try:
            certif = container.find('span', class_='certificate').get_text()
        except:
            certif = 'None'
        time = container.find('span', class_='runtime').get_text()
        genre = container.find('span', class_='genre').get_text(strip=True)
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
        vote = [item.get_text() for item in container.find_all('span',attrs={"name":"nv"})][0]
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
    liste_containers =[]
    for cont in  containers:
        liste_containers.append(extract_data(cont))
    print(liste_containers)
    with open('/Users/mac/my_workshops/SCRAPING_BS4/africanMovies/extractdata1.json', 'w') as f:
        json.dump(liste_containers, f)
    df_pandas = pd.DataFrame.from_dict(liste_containers)
    print(df_pandas)
    df_pandas.to_csv('/Users/mac/my_workshops/SCRAPING_BS4/africanMovies/movie.csv')
        
        
    
    
    

    
    