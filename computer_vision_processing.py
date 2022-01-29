import pandas as pd
import requests 
import io
from PIL import Image
import re
import os  
import random 

dataset = pd.read_excel('dataset.xlsx')
images = dataset['images']
        
df = dataset.dropna(how ='all')       
imgs = []
for i in images:
    imgs.append(i.replace("[]", "").replace("[", "").replace("]", ""))


image_list = []
for j in imgs:
    if len(j) > 1:
        s = j.split(',')
        for k in s:
            x = k.replace(" ", "")
            image_list.append(x)
    if j.startswith("{"):
        a = j.split("{'date': {'created': ")

        for b in a:
            if str("'url':") in str(b):
                c = b.split(", 'format': 'jpg', 'url':")
                d = c[1].split('}')
                e = d[0].strip()
                image_list.append(e)
    if j.startswith("'/"):
        q = j.replace("'", '')
        z = q.split(', ')
        for k in z:
            image_list.append("'https://images.yachtworld.com/resize" + k + "'")


img_list = []
for f in image_list:

    img_list.append(f[1:-1])
    
    
    
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


for f in img_list:
  
    download(f, dest_folder="images")

############################################################################################

images = []
for i in dataset['images']:
    images.append(i.replace("[]", "").replace("[", "").replace("]", ""))
images = pd.DataFrame(images)

data = pd.concat([images, dataset['model']], axis=1)
data = data.set_axis(['images', 'model'], axis=1)

data_new = data.dropna(how ='any')
data_new = data_new.set_axis(['images', 'model'], axis=1)

for i in range(len(data['model'])):
    if type(data['model'][i]) == str:
        data['model'][i] = data['model'][i].replace("/","-")
        data['model'][i] = data['model'][i].replace('"'," ")
        data['model'][i] = data['model'][i].replace("'"," ")
        data['model'][i] = data['model'][i].replace(","," ")


models = list(data['model'].unique())

def img_sep(data_model, data_image):
    
    img_list = []
    if len(data_image) > 1:
            
        if data_image.startswith("{"):
            x = data_image.replace("'", '')
            a = x.split("{date: {created: ")
            
            for b in a:
                if str("https:") in str(b):
                    c = b.split("}, format: jpg, url: ")
                    d = c[1].split('}')
                    img_list.append(d[0])
                    
        else:
            q = data_image.replace("'", '')
            s = q.split(',')
            
            for k in s:
                q = k.replace("'", '')
                w = q.replace(" ", "")
                img_list.append(w)

    return img_list


for i in range(len(data['model'])):
    if data['model'][i] in models:
    
        lst = img_sep(models[models.index(str(data['model'][i]))], data['model'][i], data['images'][i])  
        
        for f in lst:
          
            download(f, dest_folder=str(data['model'][i]))


########################################################################################################
#TEST-TRAIN-VALIDATION 
# test_size = round(int(len(dir_list))*0.33)

url = os.getcwd()
dir_list = os.listdir(url)

test = random.sample(dir_list, round(int(len(dir_list))*0.33))
train = []
for lst in dir_list:
    if lst not in test:
        train.append(lst)

# same file exist or not?
intersection = test_as_set.intersection(train)

intersection_as_test_train = list(intersection)


def train_test_Split(data_model, data_image, none_images:list):
    dir_list = img_sep(data_model, data_image)
    
    test = random.sample(dir_list, round(int(len(dir_list))*0.33))
    train = []
    for lst in dir_list:
        if lst not in test:
            train.append(lst)
            
    url = os.getcwd()
    url_train = url + "\\train"
    url_test = url + "\\test"
    none_images = []
    for tr in train:
        try:
            download(tr, dest_folder=url_train + "\\" + str(data_model))
        except:
            none_images.append(tr)
    for tst in test:
        try:
            download(tst, dest_folder=url_test + "\\" + str(data_model))
        except:
            none_images.append(tst)
        

for i in range(len(data['model'])):
    train_test_Split(data['model'][i], data['images'][i])


url = os.getcwd()
url_test = url + "\\test"
url_train = url + "\\train"

dir_list_train = os.listdir(url_train)
dir_list_test = os.listdir(url_test)


none_images = []
for i in range(len(data['model'])):
    if str(data['model'][i]) not in dir_list_train or str(data['model'][i]) not in dir_list_test:
        train_test_Split(data['model'][i], data['images'][i], none_images)
    

x_train = dir_list_train.copy()
x_test = dir_list_test.copy()
x_data = data.copy()

x = []
for i in range(len(x_data['model'])):
    if str(x_data['model'][i]) not in x_train or str(x_data['model'][i]) not in x_test:
        x.append(x_data['model'][i])

# files size checking 
dif = list(set(dir_list_train) - set(dir_list_test))

