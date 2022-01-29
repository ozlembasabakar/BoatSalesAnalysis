from bs4 import BeautifulSoup
import requests
import pandas as pd 
import os

url = 'https://www.yachtall.com/tr/tekneler?q=Nautor%20Swan'
source = requests.get(url).text

soup = BeautifulSoup(source, 'html.parser')

links = soup.find_all('div', class_='glry-box glry-active')

image_list = []
for link in links:
    image_list.append(link.find('img')['src'])
    

image_links = []
for i in range(len(image_list)):
    link_1 = str(image_list[i]).replace('//','')
    link = 'https://www.' + link_1
    image_links.append(link)


boat_models = []
for models in soup.find_all('div', class_='boatlist-content'):
    model = str(models.h3.a.text).replace('-','')
    model = model.replace('/','')
    boat_models.append(model)


image_links_df = pd.DataFrame(image_links)
boat_models_df = pd.DataFrame(boat_models)

df = pd.concat([image_links_df, boat_models_df], axis=1).set_axis(['links', 'boat_models'], axis='columns', inplace=False)

def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))


for f in range(len(df)):
  
    download(df['links'][f], dest_folder=str(df['boat_models'][f]))
    
    
    
    
    
    