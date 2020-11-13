"""
filename: helper.py
author: Supriya Sudarshan
version: 10.11.2020

description: This script consists of functions needed for the implementation of the Plagiarism checker 
"""

import nltk
import requests
from bs4 import BeautifulSoup as bs
import warnings
import re

warnings.filterwarnings('ignore')

stop_words = set(nltk.corpus.stopwords.words('english')) 

def searchEngine(query):
    """
    This function takes in the query and 
    returns the top 2 urls with content similar to query 
    """
    
    # Tokenize the query into list of words, remove stopwords from the list and join the words to form sentence(s)
    words = nltk.word_tokenize(query)
    sentences = (' '.join([word for word in words if word not in stop_words]))
    
    # Use requests to query using Google search
    url = 'https://google.com/search?q=' + sentences
    urls = []
    page = requests.get(url).text
    
    # Use Beautiful Soup to scrap all the urls with similar content as query
    soup = bs(page, 'lxml')
    for link in soup.find_all('a'):
        url = link.get('href')
        if url.startswith('/url?q'):
            s_link = url.split('=')[1]
            urls.append(s_link)
    
    return (urls[:2]) # top 2 urls

def extractFromWeb(url):
    """ This function takes in the url 
    and scraps it's text content, stores it in database.txt file"""
    
    page = requests.get(url).text
    soup = bs(page, 'html.parser')
    with open('database.txt', 'a') as f:
        for i in soup.find_all('p'):
            f.write(str(i.text))

def cosineSimilarity(query, database_file):
    """ Computes the cosine similarity between the query and the given document
    returns the similarity in percent (%) """
    
    # Get a list of all the unique words from .txt file and query
    unique_words = []
    query_l = re.sub("[^\w]", " ", query.lower()).split() 
    v1 = [unique_words.append(word) for word in query_l if word not in unique_words]
    
    with open(database_file, 'r') as f:
        database_l = re.sub("[^\w]", " ", f.read().lower()).split()
    v2 = [unique_words.append(word) for word in database_l if word not in unique_words]
    
    # Frequency counters
    query_f = []
    database_f = []
    for word in unique_words:
        qc, dc = 0,0
        
        for w in query_l:
            if w == word:
                qc += 1
        query_f.append(qc)
        
        for w in database_l:
            if w == word:
                dc += 1
        database_f.append(dc)
        
    # Compute cosine similarity using above formula
    dot_prod, query_mag, database_mag = 0,0,0
    for i in range(len(query_f)):
        dot_prod += query_f[i] * database_f[i]
        query_mag += query_f[i]**2
        
    query_mag = (query_mag)**0.5

    for i in range(len(database_f)):
        database_mag += database_f[i]**2
    database_mag = (database_mag)**0.5

    return ((float)(dot_prod / (database_mag * query_mag))*100) # match percentage

def queryWeb(text):
    
    """Takes in the query and returns the match percentage"""
    
    sites = searchEngine(text)
    matching_sites = []
    for i in sites:
        matching_sites.append(str(i).split('&')[0]) # Top 2 urls identified
    
    for i in range(len(matching_sites)):
        extractFromWeb(matching_sites[i]) # database is now ready with contents from top 2 urls
    
    matches = cosineSimilarity(text, 'database.txt') # compute similarity
    
    return (matching_sites,matches)
