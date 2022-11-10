import os
import random

pwd = os.getcwd()

def random_image(folder=None):

    if folder != None:
        files = os.listdir(pwd + '/data/samples/' + folder)
    else:
        files = os.listdir(pwd + '/data/samples')
    
    img_name = random.choice(files)

    if img_name in ['.DS_Store']:
        os.remove(img_name)
        return random_image(folder)

    if folder:
        return pwd + '/data/samples/' + folder + '/' + img_name
    else:
        return pwd + '/data/samples/' + img_name

def init_config():
    
    config = {

        "FILES_LIST" : [],
        "FILES_NAMES" : [],
        "UPLOADED_IMAGES_LIST" : [],

        "WEIGHTS_URL" : pwd + '/data/weights/yolov3_last.weights',
        "CONFIG_URL" : pwd + '/data/yolov3.cfg',
        "NAMES_URL" : pwd + '/data/classes.names',
        "DEFAULT_IMAGE_URL" : random_image(),

        "COCO_WEIGHTS_URL" : pwd + '/data/weights/yolov4.weights',
        "COCO_CONFIG_URL" : pwd + '/data/yolov4.cfg',
        "COCO_NAMES_URL" : pwd + '/data/coco.names',

        "COCO_IMG_RESOLUTION" : (416, 416),
        "COCO_CONF_THRESH" : 0.5,
        "COCO_NMS_THRESH" : 0.3,

        "LP_IMG_RESOLUTION" : (416, 416),
        "LP_CONF_THRESH" : 0.5,
        "LP_NMS_THRESH" : 0.3

    }

    return config

