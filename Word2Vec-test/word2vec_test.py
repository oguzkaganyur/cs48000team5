# Python program to generate word vectors using Word2Vec
import nltk
nltk.download('punkt')

# importing all necessary modules
from nltk.tokenize import sent_tokenize, word_tokenize
import warnings

warnings.filterwarnings(action='ignore')

import gensim
from gensim.models import Word2Vec



sample = open("found_method_names.txt", "r")
s = sample.read()

# Replaces escape character with space
f = s.replace("\n", " ")

data = [["Unity","is","a","game", "Engine", "unity2d", "unity3d", "unity"],
       ["Level","select","final","boss","beginner"],
       ["Player","move","left", "right", "movement", "controller"]]

# iterate through each sentence in the file
for i in sent_tokenize(f):
    temp = []

    # tokenize the sentence into words
    for j in word_tokenize(i):
        temp.append(j.lower())

    data.append(temp)

# Create CBOW model
model1 = gensim.models.Word2Vec(data, min_count=1, vector_size=100, window=5)

# Print results
print("Cosine similarity between 'Unity' " +
      "and 'Engine' - CBOW : ",
      model1.wv.most_similar('Unity', 'Engine'))

print("Cosine similarity between 'Unity' " +
      "and 'Spawn' - CBOW : ",
      model1.wv.most_similar('Unity', 'Spawn'))

# Create Skip Gram model
model2 = gensim.models.Word2Vec(data, min_count=1, vector_size=100, window=5, sg=1)

# Print results
print("Cosine similarity between 'Unity' " +
      "and 'Engine' - Skip Gram : ",
      model2.wv.most_similar('Unity', 'Engine'))

print("Cosine similarity between 'Unity' " +
      "and 'Spawn' - Skip Gram : ",
      model2.wv.most_similar('Unity', 'Spawn'))