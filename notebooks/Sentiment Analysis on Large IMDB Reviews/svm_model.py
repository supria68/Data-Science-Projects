"""
Prepare a SVM Model for predicting sentiments on the pickled datasets

Features: X_train, X_test 
Target: y_train, y_test [1 : positive reviews, 0 : negative reviews]

Steps:
    1. Segregate the training and testing sets from the pkl files
    2. Vectorize the features using Tf-Idf
    3. Use Support Vector Machine (SVM) with linear kernel for classifier.
    Train SVM using training sets
    4. Pickle the model for deployment
"""
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn import metrics
from sklearn.metrics import classification_report,accuracy_score

if __name__== "__main__":

    # Load the reviews from pkl files
    f = open('train.pkl', 'rb')
    reviews = pickle.load(f)
    f.close()

    f = open('test.pkl', 'rb')
    test = pickle.load(f)
    f.close()

    # Separate out the features X and target y
    X_train, y_train = reviews[0], reviews[1]
    X_test, y_test = test[0], test[1]
    
    #Generate counts from text using a vectorizer.
    vectorizer = TfidfVectorizer()
    X_train = vectorizer.fit_transform(X_train)
    X_test = vectorizer.transform(X_test)

    # Perform classification with SVM, kernel=linear
    svc_model = svm.LinearSVC()
    svc_model.fit(X_train, y_train)
    
    """
    # predict classifications for test features.
    prediction = svc_model.predict(X_test)
    print(classification_report(y_test, prediction))
    print("accuracy: {0}%".format(accuracy_score(y_test, prediction)*100))
    
    """

    # Pickle the model for deployment
    f = open('svm_model.pkl', 'wb')
    pickle.dump((svc_model, vectorizer), f, -1)
    f.close()

    print('Model is pickled and ready for deployment')
