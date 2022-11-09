import os
import random

pwd = os.getcwd()

def random_image():

    files = os.listdir(pwd + '/data/samples')
    img_name = random.choice(files)

    if img_name == '.DS_Store':
        os.remove(img_name)
        return random_image()

    return pwd + '/data/samples/' + img_name

def init_config():
    
    config = {

        "FILES_LIST" : [],
        "UPLOADED_IMAGES_LIST" : [],

        "WEIGHTS_URL" : pwd + '/data/weights/yolov3_last.weights',
        "CONFIG_URL" : pwd + '/data/yolov3.cfg',
        "NAMES_URL" : pwd + '/data/classes.names',
        "DEFAULT_IMAGE_URL" : random_image(),

        "COCO_WEIGHTS_URL" : pwd + '/data/weights/yolov4.weights',
        "COCO_CONFIG_URL" : pwd + '/data/yolov4.cfg',
        "COCO_NAMES_URL" : pwd + '/data/coco.names',

        "IMG_RESOLUTION" : (416, 416),
        "CONF_THRESH" : 0.5,
        "NMS_THRESH" : 0.3

    }

    return config

