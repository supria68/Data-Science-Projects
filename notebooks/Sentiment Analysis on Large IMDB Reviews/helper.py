"""
The script performs the following steps:
1. Fetch the data from the saved directory! (function get_data)
2. Preprocess the data and return a list of words (function preprocess)
3. Splits the data into training and testing sets, pickle it! (function main)
"""

import nltk
import re
import os
import glob
import pickle
from nltk.corpus import stopwords

dataset_path = '/notebooks/sa_imdb/datasets/' # <insert your directory>


def remove_stopwords(text):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in text:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words

def preprocess(text):
    """
    This function performs preliminary processing on textual data
    - convert to lowercase
    - remove html/url
    - remove digits or punctuations
    - tokenize the words and remove stopwords
    """
    text = text.lower() 
    text = re.sub(r'http\S+','',text) #remove url
    text = text.replace('<br />', '')
    text = text.replace('--', '')
    text = re.sub(r'[0-9]','',text)
    text = re.sub(r'[^\w\s]','',text)
    words = nltk.word_tokenize(text)
    words = remove_stopwords(words)
    
    return words

def get_data(path):
    """
    This function gets the IMDBreviews dataset, performs the preprocessing of
    the data and returns the list of words.
    """
    
    # Fetch data from the path
    sentences = []
    currdir = os.getcwd()
    os.chdir(path)
    currdir = os.getcwd()
    os.chdir(path)
    for ff in glob.glob("*.txt"):
        with open(ff, 'r') as f:
            sentences.append(f.readline().strip())
    os.chdir(currdir)
    
    # text preprocessing
    for text in sentences:
        words = preprocess(text)
    
    return words
        
if __name__ == "__main__":
    
    # Get the dataset, pre-process and split into training and testing sets
    path = dataset_path 
    
    print('Fetching the training datasets....')
    train_pos = get_data(path+'train/pos/')
    train_neg = get_data(path+'train/neg/')
    train_x = train_pos + train_neg
    train_y = [1] * len(train_pos) + [0] * len(train_neg)
    print('Fetched and preprocessed training data')
   
    print('Fetching the testing datasets....')
    test_pos = get_data(path+'test/pos')
    test_neg = get_data(path+'test/neg')
    test_x = test_pos + test_neg
    test_y = [1] * len(test_pos) + [0] * len(test_neg) 
    print('Fetched and preprocessed testing data')

    #pickle the training and testing sets for re-use
    f = open('train.pkl', 'wb')
    pickle.dump((train_x, train_y), f, -1)
    f.close()
    f = open('test.pkl', 'wb')
    pickle.dump((test_x, test_y), f, -1)
    f.close()
