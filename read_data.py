import os
import json
import pandas as pd
import datetime
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re

url = os.getcwd()
dir_list = os.listdir(url)

# print("Files and directories in '", url, "' :")
# print(dir_list)

dirName = "boats"
path = os.path.join(url, dirName)
arr = os.listdir(path)

# print("This folder has " + str(len(arr)) + " files.")

arry = []
for index in arr:
    myStr = r"C:/Users/Osman/Desktop/proje/boats/" + index + "/boat.json"
    with open(myStr, encoding = "utf8") as file:
        data = json.load(file)
        arry.append(data)
        file.close()

df = pd.DataFrame(arry)

df.drop_duplicates(subset ="id", keep = False, inplace = True)

columns = ['images', 'fullSpecs', 'title', 'make', 'model', 'location', 'currency', 'isTaxPaid', 'length', 'yearBuilt', 'price']
dataset = df.reindex(columns=columns)

print(dataset.isnull().sum())

# title, make, model

for i in range(len(dataset)):
    if dataset['make'][i] or dataset['model'][i] == 'nan':
    
        dataset['model'][i] = dataset['title'][i][5:]
        dataset['make'][i] = dataset['model'][i].split(' ')[0]

dataset = dataset.drop(columns = ["title"], axis=1)

print(dataset.isnull().sum())

# price, curency

dataset.groupby('currency')['price'].sum().sort_values(ascending=False).plot(kind='bar')
# price bilgisi en çok EUR formatında girilmiş. Birim dönüşümü yapılmalı.

for j in range(len(dataset)):
    
    if dataset['currency'][j] == '£':
        dataset['price'][j] = dataset['price'][j] * 1.3354183
        
    if dataset['currency'][j] == 'EUR':
        dataset['price'][j] = dataset['price'][j] * 1.1281847
        
    if dataset['currency'][j] == 'SEK' or dataset['currency'][j] == 'kr':
        dataset['price'][j] = dataset['price'][j] * 0.1095635

    if dataset['currency'][j] == 'NOK':
        dataset['price'][j] = dataset['price'][j] * 0.11035062
   
    if dataset['currency'][j] == 'NZ$':
        dataset['price'][j] = dataset['price'][j] * 0.68342846
    
    if dataset['currency'][j] == 'A$':
        dataset['price'][j] = dataset['price'][j] * 0.71528185
    
    if dataset['currency'][j] == 'CAN$':
        dataset['price'][j] = dataset['price'][j] * 0.78482182 

dataset = dataset.drop(columns = ["currency"], axis=1)

# location
import pytz

loc = dataset['location']
country = []

for d in dataset['location']:
    if type(d) == dict:
        country.append(str(pytz.country_names[str(d['country'])]))
    else:
        cntr = d.split(', ')
        
        if len(cntr) == 1:
            country.append(cntr[0])
        
        if len(cntr) == 2:
    
            if len(cntr[1]) == 2:
                country.append('USA')
            else:
                country.append(cntr[-1])
        
        if len(cntr) == 3:
            country.append(cntr[-1])   
            
for i in range(len(country)):
  if country[i] == 'Britain (UK)':
    country[i] = 'United Kingdom'

    
dataset['country'] = country

dataset = dataset.drop(columns = ["location"], axis=1)

# unitOfLength

for m in range(len(dataset)):
    
    if 'm' in str(dataset['length'][m]):
        t = dataset['length'][m]                  
        t1 = t.split('m')
        dataset['length'][m] = pd.to_numeric((int(t1[0]) / 0.3048), downcast='integer')
        
dataset['length'] = pd.to_numeric(dataset['length'], downcast='integer')
        
today = today = datetime.date.today()        
year = int(str(today).split('-')[0])
yearBuilt = pd.to_numeric(dataset['yearBuilt'], downcast='integer')
age = year - yearBuilt

"""
age1 = []
for r in age:
    if r > 0:
        age1.append(int(r))
"""
        
dataset['yatchAge'] = pd.DataFrame(age)        
dataset['yearBuilt'] = pd.to_numeric(dataset['yearBuilt'], downcast='integer')



fullSpecs = []
for i in range(len(dataset['fullSpecs'])):
    text = re.sub('@[A-Za-z0-9]+|[^0-9A-Za-z \t]|\w+:\/\/\S+',
                  ' ', dataset['fullSpecs'][i])
    text = text.lower()
    text = text.split()
    ps = PorterStemmer()
    all_stopwords = stopwords.words('english')
    text = [ps.stem(word) for word in text if not word in set(all_stopwords)]
    text = ' '.join(text)
    fullSpecs.append(text)

dataset['fullSpecs'] = fullSpecs        


dataset.to_excel('dataset.xlsx', index=False)
