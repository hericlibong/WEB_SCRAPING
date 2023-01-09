#intitulé : 
# sur le site : http://books.toscrape.com/ 
# récupérer le titre du livre, le  prix sans l'indiice monnaie, la couverture, le rating, la disponibilité 
# sur les toutes  les pages 
# imprimer les  données sous forme d'un  dataframe
#exporter les données en  json et csv

import requests
from  bs4  import BeautifulSoup
import pandas as  pd


    
    
    
    
def extract_data(bloc):
    title = bloc.find('a', attrs={'title': True})['title']
    cover  = bloc.find('img')['src']
    stars = bloc.find('p', attrs={'class':True})['class'][1]
    price = bloc.find('p', class_='price_color').get_text().replace('£','')
    stocks = bloc.find('p', class_='instock availability').get_text(strip=True)
    data = {
        'Title':title,
        'Cover':cover,
        'Stars':stars,
        'Price':price,
        'Stocks':stocks 
        }
    return data
    
def get_book(pageurl):
    page = requests.get(pageurl)
    soup = BeautifulSoup(page.content,  'lxml')
    blocs  = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
    if len(blocs)>0:
        liste_blocs = []
        for bloc in blocs :
            liste_blocs.append(extract_data(bloc))
        return liste_blocs
    else:
        None
data = get_book('https://books.toscrape.com/catalogue/page-1.html')
for i in range(2, 100):
    print(i)
    page_url =f'https://books.toscrape.com/catalogue/page-{i}.html'
    current_page =  get_book(page_url)
    if current_page is not None:
        data = data + current_page 
    else :
        break
print(data)
df = pd.DataFrame.from_dict(data)

    
#df = pd.DataFrame.from_dict(liste_blocs)
#print(df)
    
       

    
        
  