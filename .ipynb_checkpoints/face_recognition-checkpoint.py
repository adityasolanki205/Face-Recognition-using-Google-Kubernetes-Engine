#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import tensorflow as tf
#import mtcnn
from mtcnn.mtcnn import MTCNN
import PIL
from PIL import Image , ImageDraw, ImageFont
import numpy as np
import pandas as pd
from IPython.display import display
import os
import matplotlib.pyplot as pyplot
from tensorflow.keras.models import load_model
from sklearn.preprocessing import Normalizer, LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib 
import cv2

def load_models():
    FaceNet = load_model('models/facenet_keras.h5', compile=False)

    SVM_model = joblib.load('models/SVM_model.pkl')

    name = joblib.load('models/label.pkl')

    normalizer = Normalizer(norm = 'l2')
    detector = MTCNN()
    return FaceNet, SVM_model, name, normalizer, detector

def get_predictions(raw_image):
    FaceNet, SVM_model, name, normalizer, detector = load_models()
    nparr = np.fromstring(raw_image.data, np.uint8)
    # decode image
    image_decoded = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite('output_image/saved.jpg', image_decoded)
    image = Image.open('output_image/saved.jpg')
    #Convert the file to RGB
    image = image.convert('RGB')
    #Convert the File to Numpy array to be machine readable
    pixels = np.asarray(image)
    
    #Extracting Face embeddings from the Photo
    result = detector.detect_faces(pixels)
    #print(result)
    if len(result) == 0 :
        print ('No Face detected in this photo')
        return []
    else:
        predictions_dict = {}
        for i in range(len(result)):
            return_name = ''
            x1, y1, width, height = 0 , 0 , 0, 0
            co_ordinates = []
            x1, y1, width, height = result[i]['box']
            co_ordinates.append(x1)
            co_ordinates.append(y1)
            co_ordinates.append(width)
            co_ordinates.append(height)
            x1, y1 = abs(x1) , abs(y1)
            x2, y2 = abs(x1) + width , abs(y1) + height 
            face = pixels[y1:y2, x1:x2]
            image = Image.fromarray(face)
            image = image.resize((160,160))
            face_array = np.asarray(image)
            face_pixels = face_array.astype('float32')
            mean, std = face_pixels.mean(), face_pixels.std()
            face_pixels  = (face_pixels - mean)/std
            samples = np.expand_dims(face_pixels, axis = 0)
            output = FaceNet.predict(samples)
            embeddings = np.asarray(output)
            embeddings_normalized = normalizer.transform(embeddings)
            prediction = SVM_model.predict(embeddings_normalized)
            prob = SVM_model.predict_proba(embeddings_normalized)
            return_name = name[prediction[0]] + '_' + str(i)
            co_ordinates.append((prob.max() * 100))
            predictions_dict[return_name] = co_ordinates
    return predictions_dict

