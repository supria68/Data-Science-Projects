"""
filename: app.py
author: Supriya Sudarshan
version: 26.11.2020
description: This script takes in the backend ANN model and builds an API using
FastAPI and uvicorn
"""

import uvicorn
from fastapi import FastAPI
from base_model import ChurnModel

import numpy as np
import pandas as pd
import pickle
import tensorflow as tf

application = FastAPI()

pickle_in = open('scaler_std.pkl','rb')
scaler = pickle.load(pickle_in)

classifier = tf.keras.models.load_model('ann_model.h5')

def one_hot(geo):
    GEO_Germany, GEO_Spain  = 0, 0
    if geo == 'Germany':
        GEO_Germany, GEO_Spain  = 1, 0
    elif geo == 'Spain':
        GEO_Germany, GEO_Spain  = 0, 1
    return [GEO_Germany, GEO_Spain]

@application.get('/')
def index():
    text = 'Hey There! Welcome to my Data Science Portfolio Project.\n For predicting whether the customer exits the bank, please visit http://127.0.0.1:8000/docs/'
    return {'message': text}

@application.post('/Churn_Modelling')
def execute(data:ChurnModel):
    """
    **Bank Customer Churn Prediction**
    
    *Feature Explanation:*
    * Geography: ['France', 'Germany', 'Spain']
    * CreditScore: Current credit score of the customer
    * Gender: Male - 1, Female - 0
    * Age: Age of the customer
    * Tenure: How long has the customer stayed in the bank 
    * Balance: Existing account balance of the customer
    * NumOfProducts: How many bank products(loans, deposits...) does the customer have
    * HasCrCard: Does the customer have a credit card (Yes - 1, No - 0)
    * IsActiveMember: Is the customer an active member (Yes - 1, No - 0)
    * EstimatedSalary: Estimated Salary of the customer
    """
    data = data.dict()
    
    GEO_Germany, GEO_Spain = one_hot(data['Geography'])
    CreditScore = data['CreditScore']
    Gender = data['Gender']
    Age = data['Age']
    Tenure = data['Tenure']
    Balance = data['Balance']
    NumOfProducts = data['NumOfProducts']
    HasCrCard = data['HasCrCard']
    IsActiveMember = data['IsActiveMember']
    EstimatedSalary = data['EstimatedSalary']

    
    prediction = classifier.predict(scaler.transform([[CreditScore, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, GEO_Germany, GEO_Spain]]))

    if(prediction[0]>0.5):
        prediction="Customer Exits the Bank"
    else:
        prediction="Customer Stays at the Bank"
    
    return {
        'prediction': prediction
    }

if __name__ == '__main__':
    uvicorn.run(application, host='127.0.0.1', port=8000)
    
#uvicorn app:application --reload
