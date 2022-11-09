import streamlit as st

st.sidebar.markdown("# About ❄️")

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

def main():
    new_title = '<p style="font-size: 42px;">Welcome to my Object Detection App!</p>'
    read_me_0 = st.markdown(new_title, unsafe_allow_html=True)

    read_me = st.markdown("""
    This project was built using Streamlit and OpenCV 
    to demonstrate YOLO Object detection in both videos(pre-recorded)
    and images.
    
    
    This YOLO object Detection project can detect 80 objects(i.e classes)
    in either a video or image. The full list of the classes can be found 
    [here](https://github.com/KaranJagtiani/YOLO-Coco-Dataset-Custom-Classes-Extractor/blob/main/classes.txt)"""
    )
    st.sidebar.title("Select Activity")
    choice  = st.sidebar.selectbox("MODE",("About","Object Detection(Image)","Object Detection(Video)"))
    #["Show Instruction","Landmark identification","Show the #source code", "About"]
     

if __name__ == '__main__':
		main()	


#st.write(" Steps : ")

# - Add Multiple photos 
# - Detect if it is a car or not 
# - (OPTIONAL) Detect Smiley or unusual plate and remove it by replacing by fake plate
# - Detect the Licence Plate with poltting box and confidence intervals
# - (OPTIONAL) OCR on plate for legal checking 
# - Apply pre-Blur on Plate Box
# - Detect Lines and better blur 