#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import json
import cv2
import PIL
from PIL import Image , ImageDraw, ImageFont


url = "http://<IP address from Kubernetes>:80/predict"
headers = {"content-type": "image/jpg"}
filename = 'images/singers.jpg'
# encode image
image = cv2.imread(filename)
_, img_encoded = cv2.imencode(".jpg", image)

# send HTTP request to the server
response = requests.post(url, data=img_encoded.tostring(), headers=headers)
predictions = response.json()
print (predictions)

def font_size(width):
    thickness,font,text_add = 0,0,0
    if  width >= 700 :
        #width  = 743
        thickness  = 5
        font  = 120
        text_add = 80
    elif (width >= 650 and width < 700) :
        #width  = 660
        thickness  = 5
        font  = 110
        text_add = 60
    elif (width >= 600 and width < 650) :
        #width  = 601
        thickness  = 4
        font  = 100
        text_add = 40
    elif (width >= 550 and width < 600) :
        #width  = 527
        thickness  = 4
        font  = 85
        text_add = 35
    elif (width >= 500 and width < 550) :
        #width  = 527
        thickness  = 4
        font  = 90
        text_add = 30
    elif (width >= 450 and width < 500 ):
        # width  = 451
        thickness  = 3
        font  = 80
        text_add  = 25
    elif (width >= 400 and width < 450) :
        #width  = 380
        thickness  = 2
        font  = 73
        text_add  = 20
    elif (width >= 350 and width < 400) :
        #width  = 380
        thickness  = 2
        font  = 70
        text_add  = 20
    elif (width >= 300 and width < 350) :
        #width  = 290
        thickness  = 2
        font  = 60
        text_add  = 15
    elif (width >= 250 and width < 300) :
        #width  = 290
        thickness  = 2
        font  = 50
        text_add  = 10
    elif (width >= 200 and width < 250) :
        #width  = 238
        thickness  = 2
        font  = 40
        text_add  = 8
    else: 
        #width  = 156
        thickness  = 2
        font  = 30
        text_add  = 5
    return thickness, font , text_add 

# annotate the image
if len(predictions)== 0:
    print ('Sorry no output')
else:
    image = cv2.imread(filename)
    for i in predictions.keys():
        names = i.split('_')
        x1, y1, width, height ,percent  = 0,0,0,0, 0
        x1, y1, width, height , percent = predictions[i]
        if names[0] == 'Unknown' or percent < 60 :
            continue
        else:
            x1, y1 = abs(x1) , abs(y1)
            x2, y2 = abs(x1) + width , abs(y1) + height
            x1 -= 10
            y1 -= 10
            x2 += 10
            y2 += 10
            start_point = (x1, y2) 
            end_point = (x2, y1)
            width = x2 - x1
            # Color Order by Blue Green Red
            if names[0] == 'Aditya Solanki':
                color = (0,255, 255)#Yellow
            elif names[0] == 'Ben Afflek':
                color = (255,0, 0) #Blue
            elif names[0] == 'Elton John':
                color = (0,255, 0) #Green
            elif names[0] == 'Jerry Seinfeld':
                color = (0,0, 255) #Red
            elif names[0] == 'Madonna':
                color = (255,255, 0) #aqua
            elif names[0] == 'Mindy Kaling':
                color = (255, 255, 255) #White
            elif names[0] == 'Unknown':
                color = (0,0,0) #Black
            thickness , font, text_add = font_size(width)
            image = cv2.rectangle(image, start_point, end_point, color, thickness) 
    cv2.imwrite('output_image/recognised.jpg', image)
    image = Image.open('output_image/recognised.jpg')
    for i in predictions.keys():
        names = i.split('_')
        x1, y1, width, height ,percent  = 0,0,0,0, 0
        x1, y1, width, height , percent = predictions[i]
        if names[0] == 'Unknown' or percent < 60 :
            continue
        else:
            x1, y1 = abs(x1) , abs(y1)
            x2, y2 = abs(x1) + width , abs(y1) + height
            x1 -= 10
            y1 -= 10
            x2 += 10
            y2 += 10
            start_point = (x1, y2) 
            end_point = (x2, y1)
            width = x2 - x1
            # Color Order by Blue Green Red
            if names[0] == 'Aditya Solanki':
                color = (255,255, 0)#Yellow
                text = 'Aditya'
            elif names[0] == 'Ben Afflek':
                color = (0,0, 255) #Blue
                text = 'Ben'
            elif names[0] == 'Elton John':
                color = (0,255, 0) #Green
                text = 'Elton'
            elif names[0] == 'Jerry Seinfeld':
                color = (255,0, 0) #Red
                text = 'Jerry'
            elif names[0] == 'Madonna':
                color = (0,255, 255) #aqua
                text = 'Madonna'
            elif names[0] == 'Mindy Kaling':
                color = (255, 255, 255) #White
                text = 'Mindy'
            elif names[0] == 'Unknown':
                color = (0,0,0) #Black
                text = 'Unknown'
            thickness , font, text_add = font_size(width)
            x1_text = x1 + text_add
            y2_text = y2
            fnt = ImageFont.truetype('models/Arial.ttf', font)
            title = ImageDraw.Draw(image)
            title.text((x1_text,y2_text), text, font=fnt, fill=color)
    image.save('final.jpg')