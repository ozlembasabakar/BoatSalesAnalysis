import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recom_sys(df, df_col, input_boat):
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df_col.values.astype(str))

    # print("Count Matrix:", count_matrix.toarray())

    cosine_sim = cosine_similarity(count_matrix)

    # cosine_sim

    boat = input_boat
    def get_index_from_desc(model):
        return df[df.model == model].index.values[0]
    boat_index = get_index_from_desc(boat)

    similar_boats = list(enumerate(cosine_sim[boat_index]))

    sorted_similar_boats = sorted(similar_boats, key=lambda x:x[1], reverse=True)

    def get_desc_from_index(index):
        return df[df.index == index]["model"].values[0]

    i=0
    recom_boats = []
    for boat in sorted_similar_boats:
        recom_boats.append(get_desc_from_index(boat[0]))
        # print(get_desc_from_index(boat[0]))
        i=i+1
        if i>5:
            break
    
    return recom_boats
       
dataset = pd.read_excel('dataset.xlsx')
    
def show_recoms(func):
    recom_boats = list(func)
    return recom_boats       
    
show_recoms(recom_sys(dataset, dataset['fullSpecs'], "Grand Soleil 46"))





