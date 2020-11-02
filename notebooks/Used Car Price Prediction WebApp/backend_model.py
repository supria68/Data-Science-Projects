"""
Author: Supriya Sudarshan
Description: This script performs the machine learning modelling (backend) for used car price prediction (Germany)
Version: 27/10/2020

"""

# Basic imports
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import pickle
import warnings
warnings.filterwarnings('ignore')

"""

NOTE: For complete machine learning pipeline (Data Cleaning, Data Exploration and
Analysis, Feature Engineering, Feature Extraction, Model Selection) please
refer to the notebook 'ML_pipeline.ipynb'.

"""

# Loading the cleaned dataset
data = pd.read_csv('cleaned_car_data.csv')
data.drop(['Brand', 'Model', 'Unrepaired_damages', 'Year_of_registration'], axis = 1, inplace = True)
#print('First few rows of the cleaned dataset:')
#print(data.head())
print('\nPerforming Feature Engineering...')

# Feature Engineering for categorical data
data['Gearbox'] = data['Gearbox'].str.replace('Manual', '1').replace('Automatic', '0').astype(int)

ohe = OneHotEncoder(drop = 'first') 
ft_ohe = pd.DataFrame(ohe.fit_transform(data.Fuel_type.values.reshape(-1,1)).toarray()) # fuel type
ft_ohe.columns = ['ft_diesel','ft_electric', 'ft_hybrid', 'ft_lpg', 'ft_other', 'ft_petrol']

vt_ohe = pd.DataFrame(ohe.fit_transform(data.Vehicle_type.values.reshape(-1,1)).toarray()) # vehicle type
vt_ohe.columns = ['vt_convertible','vt_coupe', 'vt_limousine', 'vt_other', 'vt_small_car', 'vt_suv']

final_data = pd.concat([data.drop(['Vehicle_type','Fuel_type'], axis = 1), ft_ohe, vt_ohe], axis = 1)
print('\nFeature Engineering completed.')
#print('Dataset for training the model:')
#print(final_data.head())

# Train-Test Split
features  = final_data.drop('Price', axis = 1)
target = final_data['Price'] 
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size = 0.3)
print('\nTraining the regression model...')

# Model Training and Evaluation
hyp_tuned_model = RandomForestRegressor(n_estimators = 100, min_samples_split = 10,min_samples_leaf = 5, max_features = 'sqrt',max_depth = 30) # these parameters are taken from the notebook 'ML_pipeline.ipynb'
hyp_tuned_model.fit(X_train,y_train)
print('\nTraining done. Evaluating the regression model...\n')

hyp_tuned_pred = hyp_tuned_model.predict(X_test)
print("Tuned model performance on the test set: r2 score = %0.4f" %metrics.r2_score(y_test,hyp_tuned_pred))

# Save the model
file = open('regressor.pkl', 'wb')
pickle.dump(hyp_tuned_model, file)
print('\nModel saved as regressor.pkl')
