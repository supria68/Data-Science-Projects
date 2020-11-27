"""
filename: ann.py
author: Supriya Sudarshan
version: 23.11.2020
description: This script performs the construction of artificial neural network
to predict if the bank looses its existing customers or not
"""

import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

######  Loading and Data Cleaning

df = pd.read_csv('Churn_Modelling.csv')

print('\nSize of Dataset: {} rows and {} columns'.format(df.shape[0],df.shape[1]))
print('\nCheck for Null Values...')
print(df.isna().sum())
df.drop(['RowNumber', 'CustomerId', 'Surname'],axis=1, inplace = True) # Drop unnecessary columns

######   Visualization

#1. Lets check how the target is distributed in the given dataset??
df['Exited'].value_counts(normalize = True).plot(kind = 'bar')
plt.title('Distribution of Target Variable')
plt.show()

#2. Geographical countplots wrt targets
sns.countplot(x = 'Geography', data = df, hue = 'Exited')
plt.show()

#3. Gender countplots wrt target
sns.countplot(x = 'Gender', data = df, hue = 'Exited')
plt.show()

######  Feature Engineering 

# Categorical Encoding for columns 'Gender' and 'Geography'
df['Gender'] = df['Gender'].str.replace('Male','1').replace('Female', '0').astype(int)

df_x = df.drop('Exited', axis = 1)
df_x = pd.get_dummies(data = df_x,  columns=["Geography"], drop_first = True, prefix = 'GEO')

# Separating Features (X) and Target (y) Arrays
X = df_x.values 
y = df['Exited'].values 

# Weights as target is imbalanced
weights_assigned={0:1,1:4} 

# Splitting the Arrays into training and testing sets
X_train,X_test,y_train,y_test = train_test_split(X, y, test_size = 0.3)

# Scaling the features using Standard Normal Distribution
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
file = open('scaler_std.pkl', 'wb')
pickle.dump(scaler, file)

####### Implementing Artificial Neural Network using Tf2.0
model = Sequential()
model.add(Dense(30, input_dim= X_train.shape[1], activation = 'relu', kernel_initializer='he_uniform'))
model.add(Dropout(0.3))
model.add(Dense(15, activation = 'relu', kernel_initializer='he_uniform'))
model.add(Dropout(0.3))
model.add(Dense(1, activation = 'sigmoid'))

model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics =['accuracy'])

model_history = model.fit(X_train, y_train, class_weight = weights_assigned, validation_split = 0.33, epochs = 100, batch_size = 128)

print(model_history.history.keys())

# summarize history for accuracy
plt.plot(model_history.history['accuracy'])
plt.plot(model_history.history['val_accuracy'])
plt.title('ANN model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc = 0)
plt.show()

# summarize history for loss
plt.plot(model_history.history['loss'])
plt.plot(model_history.history['val_loss'])
plt.title('ANN model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc = 0)
plt.show()

###### Predictions and Evaluation
y_pred = (model.predict(X_test) > 0.5).astype('int')

from sklearn.metrics import confusion_matrix, classification_report
print('\n\nClassification report:')
print(classification_report(y_test, y_pred))
print('\nConfusion Matrix:')
print(confusion_matrix(y_test, y_pred))

from sklearn.metrics import roc_auc_score
print('\nROC-AUC score: {}'.format(roc_auc_score(y_test,y_pred)))

###### save the model
model.save('ann_model.h5')
