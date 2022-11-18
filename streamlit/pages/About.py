import streamlit as st
from config.config import random_image
import cv2

st.sidebar.markdown("# About ❄️")


#TO DO: 
# - settings for coco
# - Github link



def main():
    new_title = '<p style="font-size: 42px;">Welcome to the Licence Plate Detection App!</p>'
    read_me_0 = st.markdown(new_title, unsafe_allow_html=True)

    read_me_1 = st.markdown("""
    
    This project was built using Streamlit and OpenCV to demonstrate YOLO Object detection on images.
    

    The goal is to create a POC to demonstrate the business interest to stop homemade licence plate deletions in a car-sharing marketplace as Ouicar.
    The results with content-checking and automatic blurring are more professional and reassure guests. 


    This YOLO Licence Plate Detection project can detect if the image has a car and then detects the licence plate. 
    

    Some examples frequently found on www.ouicar.fr (reload to see more examples): 


    """
    )


    cols_img = st.columns(3)
    for index in range(len(cols_img)):
        img1 = cv2.imread(random_image(folder='homemade'))   
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB) #Apply RGB default colors
        cols_img[index].image(img1, width=int(800/len(cols_img)))



    st.sidebar.write("Made with love by @NicolasFradin")
    st.sidebar.write("Check my Github page here")


    read_me_2 = st.markdown("""


        This is some features included in this app:
        

        - Add Multiple photos 
        - Filter detection if it is a car or not 
        - Detect the Licence Plate with poltting box and confidence intervals
        - Apply pre-Blur on Plate Box
        - Detect Lines and better blur 


        A lot of improvements might be applied to raise the accuracy and results of this application:


        - Build a better labeled training & test set
        - Test multiple computer vision algorithm (ResNet50, Yolov7...)
        

        Other interesting features might be developed in the same way:


        - Car segmentation to avoid over or under-zoomed images
        - Dectect Car (Image) rotation 
        - Detect commercial car images with white background
        - Detect photoshoped Text on images
        - Detect face & body 
        - Detect Emojis or unusual plate deletion
        - Remove it by replacing by fake blurred plate
        - OCR on the plate for legal licence plate checking 
        - Check image quality

        Examples also frequetly found:

    """
    )

    cols_img = st.columns(3)
    for index in range(len(cols_img)):
        img1 = cv2.imread(random_image(folder='other_features'))   
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB) #Apply RGB default colors
        cols_img[index].image(img1, width=int(800/len(cols_img)))


    read_me_3 = st.markdown("""


        All these pre and post image uploads filters might generate stored database features about the quality of the listing. 
        And then be very usefull in the Search Rank and Risk Score algorithms.

    """
    )

if __name__ == '__main__':
		main()	
