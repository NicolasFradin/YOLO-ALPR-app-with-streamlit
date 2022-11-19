# YOLO-ALPR-app-with-streamlit:
ALPR Python app using YOLO and streamlit. This app is a ALPR POC to demonstrate an usefull feature in a car-sharing marketplace. 


#Installation:

- Create a virtual env and make:

```pip install -r requirements.txt```

- Download the darknet framework to use Yolo model at:

```!git clone https://github.com/AlexeyAB/darknet```

- You can use this free French plates dataset to train Yolo: 

```!git clone https://github.com/qanastek/FrenchLicencePlateDataset.git```

- If you want to use your own images, you can use this tool to label:

```!git clone https://github.com/heartexlabs/labelImg.git```


#Scrapy
To scrap many car images you can use the scrapy porject I joined directly in this repo. 
Use:
	 ```scrapy crawl car-spider```


# Download Weights:
Yolo weights are too large to be pushed on Github. You need to download pre-trained weights by your own and train the algorithm by yourself. Use this command:

```!wget https://pjreddie.com/media/files/darknet53.conv.74```

You can check the Notebook I've developed to understand how to do it easily with your own images. 


# Streamlit application:
To launch the streamlit application make:

```streamlit run streamlit/app.py```


![alt text](https://github.com/NicolasFradin/YOLO-ALPR-app-with-streamlit/blob/master/app-screen.png)

![alt text](https://github.com/NicolasFradin/YOLO-ALPR-app-with-streamlit/blob/master/app-screen-2.png)




