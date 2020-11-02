"""
Author: Supriya Sudarshan
Description: This script performs the machine learning model deployment using Flask for used car price prediction (Germany)
Version: 27/10/2020

"""

# Basic imports
from flask import Flask, render_template, request
import requests
import pickle
import numpy as np
import sklearn


app = Flask(__name__)

# loading the backend model
model = pickle.load(open('regressor.pkl', 'rb'))

@app.route('/',methods=['GET'])

def Home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])

def predict():
    [ft_diesel,ft_electric, ft_hybrid, ft_lpg, ft_other, ft_petrol] = [0,0,0,0,0,0]
    [vt_convertible,vt_coupe, vt_limousine, vt_other, vt_small_car, vt_suv] = [0,0,0,0,0,0]

    if request.method == 'POST':

        Gearbox = request.form['Gearbox']
        if(Gearbox == 'Manual'):
            Gearbox = 1
        else:
            Gearbox = 0

        Kms_driven = float(request.form['Kms_driven'])

        Year = int(request.form['Year'])


        Fuel_type = request.form['Fuel_Type']
        if(Fuel_type == 'Petrol'):
            [ft_diesel,ft_electric, ft_hybrid, ft_lpg, ft_other, ft_petrol] = [0,0,0,0,0,1]
        elif(Fuel_type == 'Diesel'):
            [ft_diesel,ft_electric, ft_hybrid, ft_lpg, ft_other, ft_petrol] = [1,0,0,0,0,0]
        elif(Fuel_type == 'Electric'):
            [ft_diesel,ft_electric, ft_hybrid, ft_lpg, ft_other, ft_petrol] = [0,1,0,0,0,0]
        elif(Fuel_type == 'Hybrid'):
            [ft_diesel,ft_electric, ft_hybrid, ft_lpg, ft_other, ft_petrol] = [0,0,1,0,0,0]
        elif(Fuel_type == 'lpg'):
            [ft_diesel,ft_electric, ft_hybrid, ft_lpg, ft_other, ft_petrol] = [0,0,0,1,0,0]
        elif(Fuel_type == 'other'):
            [ft_diesel,ft_electric, ft_hybrid, ft_lpg, ft_other, ft_petrol] = [0,0,0,0,1,0]
        
        Vehicle_type = request.form['Vehical_Type']
        if(Vehicle_type == 'limousine'):
            [vt_convertible,vt_coupe, vt_limousine, vt_other, vt_small_car, vt_suv] = [0,0,1,0,0,0]
        elif(Vehicle_type == 'Coupe'):
            [vt_convertible,vt_coupe, vt_limousine, vt_other, vt_small_car, vt_suv] = [0,1,0,0,0,0]
        elif(Vehicle_type == 'Convertible'):
            [vt_convertible,vt_coupe, vt_limousine, vt_other, vt_small_car, vt_suv] = [1,0,0,0,0,0]
        elif(Vehicle_type == 'Other'):
            [vt_convertible,vt_coupe, vt_limousine, vt_other, vt_small_car, vt_suv] = [0,0,0,1,0,0]
        elif(Vehicle_type == 'Small car'):
            [vt_convertible,vt_coupe, vt_limousine, vt_other, vt_small_car, vt_suv] = [0,0,0,0,1,0]
        elif(Vehicle_type == 'SUV'):
            [vt_convertible,vt_coupe, vt_limousine, vt_other, vt_small_car, vt_suv] = [0,0,0,0,0,1]
        
        Age_of_car = 2020 - Year

        
        prediction = model.predict([[Gearbox, Kms_driven, Age_of_car, ft_diesel,ft_electric, ft_hybrid, ft_lpg, ft_other, ft_petrol, vt_convertible,vt_coupe, vt_limousine, vt_other, vt_small_car, vt_suv]])

        output = round(prediction[0],2)

        if output < 0 or Age_of_car == 0:
            return render_template('index.html',prediction_text = "Please re-enter correct values...")
        else:
            return render_template('index.html',prediction_text = "You can buy or sell the car at {} €".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug = True)    
