# -*- coding: utf-8 -*-
"""Fake_News_Detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19T64WBIQGFobUgwRgJcApA9AoUroS_HI
"""

import pandas as pd

data = pd.read_csv('/content/fake_news_train.csv',error_bad_lines=False, engine="python")

data.head()

import numpy as np
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import nltk
nltk.download('stopwords')

print(stopwords.words('english'))

data.isnull().sum()

data = data.fillna('')

data['content'] = data['author'] + ' ' + data['text']

data.head()

X = data.drop("label", axis = 1)
Y = data['label']

print(X)

port_stem = PorterStemmer()

def stemming(content):
    stemmed_content = re.sub('[^a-zA-Z]',' ',content)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split()
    stemmed_content = [port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
    stemmed_content = ' '.join(stemmed_content)
    return stemmed_content

data['content'] = data['content'].apply(stemming)

X = data['content'].values
Y = data['label']

print(X)

vectorizer = TfidfVectorizer()
vectorizer.fit(X)
X = vectorizer.transform(X)

print(X)

X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.3,stratify=Y,random_state=1)

model = LogisticRegression()

model.fit(X_train, Y_train)

X_train_prediction = model.predict(X_train)
train_accuracy = accuracy_score(X_train_prediction, Y_train)
print("Accuracy: ",train_accuracy)

X_test_prediction = model.predict(X_test)
test_accuracy = accuracy_score(X_test_prediction, Y_test)
print("Accuracy: ",test_accuracy)

