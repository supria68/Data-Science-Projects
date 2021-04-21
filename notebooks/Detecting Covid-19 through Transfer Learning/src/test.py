"""
filename: test.py
author: Supriya Sudarshan
version: 19.04.2021
description: Takes in the images and predicts (Covid or Non-Covid/Normal) using the *.h5 models  
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg19 import preprocess_input 
import random


def evaluate(img_path, model):
    """
    Given the image path and model, preprocess the input image and get
    predictions
    """
    img = image.load_img(img_path, target_size=(224,224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    image_data = preprocess_input(x)

    y_pred = model.predict(image_data)
    probability = y_pred[0]
    if probability[0] > 0.5:
        prediction = str('%.2f' % (probability[0]*100) + '% COVID') 
    else:
        prediction = str('%.2f' % ((1-probability[0])*100) + '% Normal')
    
    plt.title(prediction)
    plt.imshow(img)
    plt.show()


if __name__ == "__main__":
    
    # Load appropriate models
    ct_model = load_model('../saved_models/chest_ct_vggmodel.h5')
    xray_model = load_model('../saved_models/chest_xray_vggmodel.h5')
    ultrasound_model = load_model('../saved_models/ultrasound_vggmodel.h5')

    
    ##### Predictions CT
    path = '../images_for_testing/CT'

    img = random.choice([x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))])
    print('\nPreparing to predict for a CT image: {}'.format(img))
    evaluate(path + '/'+ img, ct_model)

    ##### Predictions Xray
    path = '../images_for_testing/Xray'

    img = random.choice([x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))])
    print('\nPreparing to predict for a Xray image: {}'.format(img))
    evaluate(path + '/'+ img, xray_model)

    ##### Predictions Ultrasound
    path = '../images_for_testing/Ultrasound'

    img = random.choice([x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))])
    print('\nPreparing to predict for a ultrasound image: {}'.format(img))
    evaluate(path + '/'+ img, ultrasound_model)
