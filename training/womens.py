import requests
from bs4 import BeautifulSoup
import pandas as pd

    
def extract_data(data_list):
        product = data_list.find('h3').get_text()
        price =  data_list.find('span',  class_='price').get_text().replace('€', '')
        data =  {
            'Product':product,
            'Price' :price
            }
        return data

def get_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    container = soup.find_all('div', class_='collection_desc clearfix')
    if len(container)>0:
        liste_container=[extract_data(cont) for cont in  container]
        return liste_container
    else:
        return None            
        
data = get_url('http://formation-data.com/?product_cat=women')
for i in range(2, 10):
    print(i)
    page_url = f'http://formation-data.com/?product_cat=women&paged={i}'
    current_page = get_url(page_url)
    if current_page is  not None:
        data = data + current_page
    else:
        break
#print(data)
df =  pd.DataFrame.from_dict(data)
print(df)
print(df.shape)        
    