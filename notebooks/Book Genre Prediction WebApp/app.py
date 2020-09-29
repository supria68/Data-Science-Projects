"""
Script for deploying the model
"""

# Importing essential libraries
from flask import Flask, render_template, request
import pickle

# Load the pickle file 
f = 'genrePrediction.pkl'
myfiles = pickle.load(open(f, 'rb'))

# Segregate the encoder, logistic regression model and the vectorsorizer
le, lr_model, vectorizer = myfiles[0], myfiles[1], myfiles[2]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods = ['POST'])
def predict():
    if request.method == 'POST':
        message = request.form['message']
        input_features=[message]
        vectors = vectorizer.transform(input_features)
        model_prediction = lr_model.predict(vectors)
        pred = le.inverse_transform(model_prediction)
        return render_template('index.html', prediction_texts= "Genre: {}".format(pred))

if __name__ == '__main__':
    app.run(debug = True)
