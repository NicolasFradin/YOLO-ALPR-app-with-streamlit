#execute "streamlit run app.py" to run the app

import json
import logging
from pickle import load
import numpy as np
import pandas as pd
import requests
import streamlit as st
from PIL import Image, ImageEnhance
import cv2
import os
import urllib
import time
import sys
import imutils 
import matplotlib.pyplot as plt 
import warnings
warnings.filterwarnings('ignore')

from config.config import init_config, random_image, delete_sample_image

st.sidebar.markdown("# Licence Plate ❄️")
st.title('Licence Plate Detection for Images')
st.subheader("""
This object detection project takes in an image and outputs the image with bounding boxes created around licence plate
""")
st.markdown("""

	How it works? 

	- Upload one or multiple images (or use the random test image button)
	- Click on the 'Go!' button to start the detection

    """
    )


if len(st.session_state.keys()) > 0:
	#st.write(st.session_state)
	pass
	
else:
	config = init_config()
	for key in config.keys():
		st.session_state[key] = config[key]
	#st.write(st.session_state)


col1, col2, col3 = st.columns(3)

with col1:
	file = st.file_uploader('', type = ['jpg','png','jpeg'])
	if file and file not in st.session_state.FILES_LIST:
		st.session_state.FILES_LIST.append(file)

with col2:
	st.write("OR")

with col3:
	test_button = st.button('Test Image')





img1 = None
if len(st.session_state.FILES_LIST) > 0:

	cols_img = st.columns(len(st.session_state.FILES_LIST))
	for index, file in enumerate(st.session_state.FILES_LIST):

		img1 = Image.open(file)
		cols_img[index].image(img1, width=int(600/len(cols_img)), caption = "Uploaded Image")
		#my_bar = st.progress(0)
		img1 = np.array(img1.convert('RGB'))
		
		st.session_state.FILES_NAMES.append(file.name)
		st.session_state.UPLOADED_IMAGES_LIST.append(img1)


if test_button:

	#Remove images cache
	st.session_state.FILES_LIST = []
	st.session_state.FILES_NAMES = []
	st.session_state.UPLOADED_IMAGES_LIST = []

	cols_img = ["col1"]
	st.session_state.DEFAULT_IMAGE_URL = random_image()
	img1 = cv2.imread(st.session_state.DEFAULT_IMAGE_URL)	
	img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB) #Apply RGB default colors
	st.image(img1, width=int(600/len(cols_img)), caption = "Uploaded Image")
	st.session_state.UPLOADED_IMAGES_LIST.append(img1)



def licence_plate_detection(img):

	img_with_boxes = img.copy()
	img_with_blur = img.copy()

	# Load the network using openCV
	net = cv2.dnn.readNetFromDarknet(st.session_state.CONFIG_URL, st.session_state.WEIGHTS_URL)
	net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
	net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

	# Get the output layer from YOLOv3
	layers = net.getLayerNames()
	#print(layers)
	print(net.getUnconnectedOutLayers())
	output_layers = [layers[i - 1] for i in net.getUnconnectedOutLayers()]
	print("output_layers :", output_layers)

	#Convert the image to blob
	height, width = img.shape[:2]
	blob = cv2.dnn.blobFromImage(img, 1 / 255, st.session_state.LP_IMG_RESOLUTION, (0, 0, 0), swapRB=True, crop=False)   #Mean subtraction + Scaling by some factor
	#print("blob :", blob)

	#Foward pass
	net.setInput(blob)
	layer_outputs = net.forward(output_layers)


	#Get all detected boxes 
	class_ids, confidences, b_boxes = [], [], []
	for output in layer_outputs:
		for detection in output:
			scores = detection[5:]
			class_id = np.argmax(scores)
			confidence = scores[class_id]

			
			if confidence > st.session_state.LP_CONF_THRESH:
			  # print("confidence :", confidence)
			  center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')
			  x = int(center_x - w / 2) 
			  y = int(center_y - h / 2)
			  b_boxes.append([x, y, int(w), int(h)])
			  confidences.append(float(confidence))
			  class_ids.append(int(class_id))


	print("b_boxes :", b_boxes)
	print("confidences :", confidences)


	# Perform non maximum suppression for the bounding boxes to filter overlapping and low confident bounding boxes
	indices = cv2.dnn.NMSBoxes(b_boxes, confidences, st.session_state.LP_CONF_THRESH, st.session_state.LP_NMS_THRESH) #.flatten().tolist()     #non-maximum suppression given boxes and corresponding scores
	#print(indices)

	# Draw the filtered bounding boxes with their class to the image
	if len(indices) > 0:

		#Load classes (here only LP)
		with open(st.session_state.NAMES_URL, "r") as f:
			classes = [line.strip() for line in f.readlines()]
		
		colors = np.random.uniform(0, 255, size=(len(classes), 3))
		
		for index in indices:
			(x, y) = (b_boxes[index][0], b_boxes[index][1])
			(w, h) = (b_boxes[index][2], b_boxes[index][3])
			
			# print("x :", x)
			# print("y :", y)
			# print("w :", w)
			# print("h :", h)

			if x < 0: x=0
			if y < 0: y=0
			if w < 0: w=0
			if h < 0: h=0

			#Add rectangle of the box
			cv2.rectangle(img_with_boxes, (x, y), (x + w, y + h), (0, 255, 0), 2)          
			
			#Add text & confidence score
			text = "{}: {:.4f}".format("LP: ", confidences[index])
			cv2.putText(img_with_boxes, text, (x, y - 3), cv2.FONT_HERSHEY_COMPLEX_SMALL, .75 , (0, 255, 0), 1)

		st.image(img_with_boxes, width=int(600/len(st.session_state.UPLOADED_IMAGES_LIST)), caption = "Boxes Predicted")

		for index in indices:
			(x,y) = (b_boxes[index][0], b_boxes[index][1])
			(w,h) = (b_boxes[index][2], b_boxes[index][3])
			
			if x < 0: x=0
			if y < 0: y=0
			if w < 0: w=0
			if h < 0: h=0

			# Blur the ROI of the detected licence plate
			img_with_blur[y:y+h, x:x+w] = cv2.GaussianBlur(img_with_blur[y:y+h, x:x+w] , (55,55), 0)
			
		st.image(img_with_blur, width=int(600/len(st.session_state.UPLOADED_IMAGES_LIST)), caption = "LP Blurred")

	else: 
		
		delete_sample_image(st.session_state.DEFAULT_IMAGE_URL)
		print("deleted: ", st.session_state.DEFAULT_IMAGE_URL)

		st.write("NO PLATE DETECTED...")
		st.write("Try to raise thresholds to detect the plate...")



def car_detection(img):

	img_with_boxes = img.copy()

	# Load the network using openCV
	net = cv2.dnn.readNetFromDarknet(st.session_state.COCO_CONFIG_URL, st.session_state.COCO_WEIGHTS_URL)
	net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
	net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

	# Get the output layer from YOLOv3
	layers = net.getLayerNames()
	# print(layers)
	# print(net.getUnconnectedOutLayers())
	#output_layers = [layers[i - 1] for i in net.getUnconnectedOutLayers()]
	output_layers = [layers[i - 1] for i in net.getUnconnectedOutLayers()]

	# print("output_layers :", output_layers)

	#Convert the image to blob
	height, width = img.shape[:2]
	blob = cv2.dnn.blobFromImage(img, 1 / 255, st.session_state.LP_IMG_RESOLUTION, (0, 0, 0), swapRB=True, crop=False)   #Mean subtraction + Scaling by some factor
	#print("blob :", blob)

	#Foward pass
	net.setInput(blob)
	layer_outputs = net.forward(output_layers)


	#Get all detected boxes 
	class_ids, confidences, b_boxes = [], [], []
	for output in layer_outputs:
		for detection in output:
			scores = detection[5:]
			class_id = np.argmax(scores)
			confidence = scores[class_id]

			
			if confidence > st.session_state.COCO_CONF_THRESH:
			  # print("confidence :", confidence)
			  center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')
			  x = int(center_x - w / 2) 
			  y = int(center_y - h / 2)
			  b_boxes.append([x, y, int(w), int(h)])
			  confidences.append(float(confidence))
			  class_ids.append(int(class_id))


	# print("b_boxes :", b_boxes)
	# print("confidences :", confidences)


	# Perform non maximum suppression for the bounding boxes to filter overlapping and low confident bounding boxes
	indices = cv2.dnn.NMSBoxes(b_boxes, confidences, st.session_state.COCO_CONF_THRESH, st.session_state.COCO_NMS_THRESH) #.flatten().tolist()     #non-maximum suppression given boxes and corresponding scores
	#print(indices)

	# Draw the filtered bounding boxes with their class to the image
	if len(indices) > 0:

		#Load classes (here only LP)
		with open(st.session_state.COCO_NAMES_URL, "r") as f:
			classes = [line.strip() for line in f.readlines()]
		
		colors = np.random.uniform(0, 255, size=(len(classes), 3))
		
		for index in indices:
			(x, y) = (b_boxes[index][0], b_boxes[index][1])
			(w, h) = (b_boxes[index][2], b_boxes[index][3])
			
			# print("x :", x)
			# print("y :", y)
			# print("w :", w)
			# print("h :", h)

			if x < 0: x=0
			if y < 0: y=0
			if w < 0: w=0
			if h < 0: h=0

			#Add rectangle of the box
			cv2.rectangle(img_with_boxes, (x, y), (x + w, y + h), (255, 0, 0), 2)          
			
			#Add text & confidence score
			text = "{}: {:.4f}".format("CAR: ", confidences[index])
			cv2.putText(img_with_boxes, text, (x, y - 3), cv2.FONT_HERSHEY_COMPLEX_SMALL, .75 , (255, 0, 0), 1)

		st.image(img_with_boxes, caption = "Boxes Predicted")

		return True
	
	else: 
		st.write("NO CAR FOUND IN THIS IMAGE...")
		st.write("Try to raise thresholds to detect the car...")
		return False


button_next = st.button('Go !')

if st.session_state is not {} and button_next:
	
	# Read the image
	for uploaded_image in st.session_state.UPLOADED_IMAGES_LIST:
		img = uploaded_image.copy()

		#Processing of the image 
		#gray_img = cv2.cvtColor(st.session_state.uploaded_img, cv2.COLOR_BGR2GRAY)
		#st.image(gray_img, caption = "Grayscaled Image")

		#Check if it is a car 
		car_detected = car_detection(img)

		#Detect the LP
		if car_detected:
			licence_plate_detection(img)


	#Remove images cache
	st.session_state.FILES_LIST = []
	st.session_state.FILES_NAMES = []
	st.session_state.UPLOADED_IMAGES_LIST = []




