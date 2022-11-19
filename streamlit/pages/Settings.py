import streamlit as st
import os 
import time 
from config.config import init_config


st.sidebar.markdown("# Settings ❄️")


st.write("CAR:")
COCO_CONF_THRESH = st.slider('Confidence Threshold (%)', 0, 100, 50),
COCO_NMS_THRESH = st.slider('NMS Threshold (%)', 0, 100, 20)
COCO_IMG_RESOLUTION = st.radio("Image Resolution", ('320×320', '416x416', '609×609'))

st.write("LICENCE PLATE:")
CONF_THRESH = st.slider('LP Confidence Threshold (%)', 0, 100, 50),
NMS_THRESH = st.slider('LP NMS Threshold (%)', 0, 100, 20)
IMG_RESOLUTION = st.radio("LP Image Resolution", ('320×320', '416x416', '609×609'))



button = st.button('Apply')

config = init_config()

if button:

    config["CONF_THRESH"] = CONF_THRESH[0] / 100 if isinstance(CONF_THRESH, tuple) else CONF_THRESH / 100
    config["NMS_THRESH"] = NMS_THRESH[0] / 100 if isinstance(NMS_THRESH, tuple) else NMS_THRESH / 100
    config["COCO_CONF_THRESH"] = COCO_CONF_THRESH[0] / 100 if isinstance(COCO_CONF_THRESH, tuple) else COCO_CONF_THRESH / 100
    config["COCO_NMS_THRESH"] = COCO_NMS_THRESH[0] / 100 if isinstance(COCO_NMS_THRESH, tuple) else COCO_NMS_THRESH / 100

    for key in config.keys():
        st.session_state[key] = config[key]

    time.sleep(1.2)
    apply_text = st.markdown("DONE !")
    time.sleep(0.8)
    apply_text.empty()

    st.markdown("Parameters saved :")
    st.write(st.session_state)


