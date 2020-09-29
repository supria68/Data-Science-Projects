"""
Script for deploying the machine learning model
"""

import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Loading the dataset
books = pd.read_csv('book_list.csv', encoding = "ISO-8859-1", names = ['Id', 'Image', 'Image_link', 'Title', 'Author', 'Class', 'Genre'])

# Encoding the 'Genre'
le = LabelEncoder()
genre_cat = le.fit_transform(books['Genre']) # Encoded Genres
genre = le.inverse_transform(genre_cat) # Original Genres

# Processing 'Title' - remove stopwords and vectorize

stop_words = list(stopwords.words('english'))
def change(title):
    return ' '.join([word for word in title if word not in stop_words])
books['title_alt'] = pd.DataFrame(books['Title'])
books['title_alt'].apply(change)


vectorizer = TfidfVectorizer(max_features = 50000, strip_accents = 'unicode', lowercase = True, analyzer = 'word', token_pattern = r'\w+', use_idf = True, smooth_idf = True, sublinear_tf = True, stop_words = 'english')
vectors = vectorizer.fit_transform(books['title_alt'])

# splitting the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(vectors, genre_cat, test_size = 0.2)

# Training a Logistic Regressor
lr = LogisticRegression(solver = 'sag', max_iter = 200)
lr.fit(X_train, y_train)

# pickle the trained model and vectorizer!
f = open('genrePrediction.pkl','wb')
pickle.dump((le, lr, vectorizer), f, -1)
f.close()

print('Job completed... Model is ready to be deployed')
