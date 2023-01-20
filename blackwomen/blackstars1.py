from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import urljoin


    
def extract_data(container):
    name = container.find('h3', class_='lister-item-header').find('a').get_text()
    detail_link = urljoin('https://www.imdb.com',container.find('div', class_='lister-item-image').find('a')['href'])
    image_link = container.find('div', class_='lister-item-image').find('img')['src']
    try :
        title = container.find_previous('p', class_='text-muted text-small').get_text(strip=True)
    except:
        title = None
    try:
        desc = [p.get_text() for p in container.find_all('p')][1]
    except:
        desc = None
    data = {
        'name':name,
        'link':detail_link,
        'title':title,
        'image': image_link,
        'desc':desc
    }
    return data

def get_item(page_url):
    page = requests.get(page_url)
    parsed_page = BeautifulSoup(page.content, 'lxml')
    containers = parsed_page.find_all('div', class_='lister-item mode-detail')
    if len(containers)>0:
        list_containers = [extract_data(cont) for cont in containers]
        return list_containers
    else:
        return None
data = get_item('https://www.imdb.com/list/ls066061932/')
for i in range(2, 100):
    print(i)
    page_url = f'https://www.imdb.com/list/ls066061932/?sort=list_order,asc&mode=detail&page={i}&ref_=nmls_vm_dtl'
    current_page = get_item(page_url)
    if  current_page is not None:
        data  = data + current_page
    else:
        break

data_pd = pd.DataFrame.from_dict(data)
print(data_pd)


data_pd.to_csv('//Users/mac/my_workshops/freelancework/blackwomen/blackstars.csv')
    
    
    
    
    
    
    
    
    
# Name
# Link to profile page
# Link to Image
# Short description
# Long description