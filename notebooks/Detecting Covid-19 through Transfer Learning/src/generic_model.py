"""
filename: generic_model.py
author: Supriya Sudarshan
version: 15.04.2021
description: helper functions (plotting, report generation, vgg base model)
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
import cv2

from glob import glob

from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.utils import to_categorical

from tensorflow.keras.layers import Input, Dense, Flatten, Dropout
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.applications import VGG19
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def split_images_and_process(covid_files, normal_files):
    print('Total number of covid images: {}'.format(len(covid_files)))
    print('Total number of non-covid images: {}'.format(len(normal_files)))

    # Preparing Labels
    covid_labels = []
    normal_labels = []

    covid_images=[]
    normal_images=[]


    for i in range(len(covid_files)):
        image = cv2.imread(covid_files[i])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image,(224,224))
        covid_images.append(image)
        covid_labels.append('Covid')
    for i in range(len(normal_files)):
        image = cv2.imread(normal_files[i])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image,(224,224))
        normal_images.append(image)
        normal_labels.append('Normal')

    # Convert to array and Normalize to interval of [0,1]
    covid_images = np.array(covid_images) / 255
    normal_images = np.array(normal_images) / 255

    # split into training and testing
    covid_x_train, covid_x_test, covid_y_train, covid_y_test = train_test_split(covid_images, covid_labels, test_size=0.2)
    normal_x_train, normal_x_test, normal_y_train, normal_y_test = train_test_split(normal_images, normal_labels, test_size=0.2)


    X_train = np.concatenate((normal_x_train, covid_x_train), axis=0)
    X_test = np.concatenate((normal_x_test, covid_x_test), axis=0)
    y_train = np.concatenate((normal_y_train, covid_y_train), axis=0)
    y_test = np.concatenate((normal_y_test, covid_y_test), axis=0)

    # make labels into categories - either 0 or 1
    lb = LabelBinarizer()
    #print(y_train[0])
    y_train = lb.fit_transform(y_train)
    #print(y_train[0])
    y_train = to_categorical(y_train)
    #print(y_train[0])

    y_test = lb.transform(y_test)
    y_test = to_categorical(y_test)

    return [X_train, X_test, y_train, y_test]

def vgg_model(lr=1e-3, dropout_val=0.2, fc_neurons=64):
    
    vggModel = VGG19(weights="imagenet", include_top=False,input_tensor=Input(shape=(224, 224, 3)))
    
    outputs = vggModel.output
    outputs = Flatten()(outputs)
    outputs = Dense(fc_neurons, activation='relu')(outputs)
    outputs = Dropout(dropout_val)(outputs)
    outputs = Dense(2, activation='softmax')(outputs)

    model = Model(inputs=vggModel.input, outputs=outputs)

    for layer in vggModel.layers:
        layer.trainable = False

    opt = tf.keras.optimizers.Adam(learning_rate = lr) 

    model.compile(loss='binary_crossentropy',optimizer=opt, metrics=['accuracy'])

    return model

def plot_model_acc_loss(history, title):
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])

    plt.title(title)
    plt.ylabel('Accuracy/Loss')
    plt.xlabel('Epoch')

    plt.legend(['train_acc','val_acc','train_loss','val_loss'])
    plt.show()

def plot_confusion_matrix(classes, y_true, y_pred):
    tick_marks = [0.5,1.5]
    cn = confusion_matrix(y_true, y_pred)
    sns.heatmap(cn,cmap='plasma',annot=True)
    plt.xticks(tick_marks, classes)
    plt.yticks(tick_marks, classes)
    plt.title('Confusion Matrix')
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()

def report(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()

    acc = (tp + tn)/np.sum(cm)
    sens = tp/(tp + fn)
    spec = tn/(fp + tn)
    prec = tp/(tp + fp)
    rec = tp/(tp + fn)

    f1 = (2*prec*rec)/(prec + rec) 
    auc = roc_auc_score(y_true, y_pred)

    print("\nAccuracy: ", acc)
    print("Sensitivity: ", sens)
    print("Specificity: ", spec)
    print("Precision: ", prec)
    print("Recall: ", rec)
    print("F1 Score: ", f1)
    print("AUC Score: ", auc)

    print("\nClassification report:")
    print(classification_report(y_true, y_pred))



