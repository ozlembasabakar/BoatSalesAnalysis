# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 12:47:40 2021

@author: Osman
"""
import pandas as pd
import missingno as msno
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

dataset = pd.read_csv('boat_dataset.csv')

dataset = dataset.drop([3472])
dataset = dataset.drop(['state'], axis=1) # 2000 küsür boş değer vardı

msno.bar(dataset)

# isTaxPaid -> Label Encoder
# fuel -> One-Hot Encoder
# engine -> Label Encoder
# country -> One-Hot Encoder
# city -> One-Hot Encoder
# make -> One-Hot Encoder

def impute_nan_most_frequent_category(DataFrame,ColName):
     most_frequent_category=DataFrame[ColName].mode()[0]
    
     DataFrame[ColName + "_Imputed"] = DataFrame[ColName]
     DataFrame[ColName + "_Imputed"].fillna(most_frequent_category,inplace=True)
     
for Columns in ['fuel']:
    impute_nan_most_frequent_category(dataset,'fuel')
 
for Columns in ['engine']:
    impute_nan_most_frequent_category(dataset,'engine')
    
for Columns in ['city']:
    impute_nan_most_frequent_category(dataset,'city')

dataset['fuel'] = dataset['fuel_Imputed']
dataset['engine'] = dataset['engine_Imputed']
dataset['city'] = dataset['city_Imputed']

dataset = dataset.drop(['fuel_Imputed', 'engine_Imputed', 'city_Imputed'], axis=1) 

# Correlation between isTaxPaid, sellerAgency and price

dataset['isTaxPaid_cat'] = dataset['isTaxPaid'].astype('category').cat.codes
dataset['sellerAgency_cat'] = dataset['sellerAgency'].astype('category').cat.codes

corr = dataset.corr()

for Columns in ['isTaxPaid']:
    impute_nan_most_frequent_category(dataset,'isTaxPaid')
 
for Columns in ['sellerAgency']:
    impute_nan_most_frequent_category(dataset,'sellerAgency')

dataset['isTaxPaid_imp_cat'] = dataset['isTaxPaid'].astype('category').cat.codes
dataset['sellerAgency_imp_cat'] = dataset['sellerAgency'].astype('category').cat.codes

corr = dataset.corr()["price"].sort_values(ascending=False).head(20)

dataset = dataset.drop(['sellerAgency', 'isTaxPaid', 'isTaxPaid_cat', 'sellerAgency_cat'
                        , 'isTaxPaid_imp_cat', 'sellerAgency_imp_cat', 'isTaxPaid_Imputed', 'sellerAgency_Imputed'], axis=1)

#  Feature engineering - Hand made feature
description = pd.read_csv('description.csv')

# boat type
dataset.loc[(dataset['length'] <= 16), 'boatType']= 'class_I'
dataset.loc[(dataset['length'] > 16) & (dataset['length'] < 26), 'boatType']= 'class_II'
dataset.loc[(dataset['length'] >= 26) & (dataset['length'] < 40), 'boatType']= 'class_III'
dataset.loc[(dataset['length'] >= 40) & (dataset['length'] < 65), 'boatType']= 'class_IV'
dataset.loc[(dataset['length'] >= 65) & (dataset['length'] < 100), 'boatType']= 'class_V'
dataset.loc[(dataset['length'] >= 100), 'boatType']= 'class_VI'

dataset["yacthAge"] = 2021 - dataset["yearBuilt"]

dataset.loc[(dataset['fuel'] == 'Diesel'), 'ecoBoats'] = 'True'
dataset.loc[(dataset['fuel'] == 'Gas/Petrol'), 'ecoBoats'] = 'False'
dataset.loc[(dataset['fuel'] == 'Other'), 'ecoBoats'] = 'Other'

y = dataset['price']
X = dataset.drop(['price'], axis=1)

# Outliers
plt.figure(figsize=(5,5))
sns.boxplot(y='price',data=dataset)

Q1 = dataset.quantile(0.25)
Q3 = dataset.quantile(0.75)
IQR = Q3 - Q1
print(IQR)

dataset_out = dataset[~((dataset < (Q1 - 1.5 * IQR)) |(dataset > (Q3 + 1.5 * IQR))).any(axis=1)]

plt.figure(figsize=(5,5))
sns.boxplot(y='price',data=dataset_out)
