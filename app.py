import streamlit as st
import cv2
import numpy as np
import av
import torch
import tempfile
from PIL import Image

@st.cache_resource
def load_model():
  model_url = "https://github.com/Fachriadr/katarak/blob/main/best.pt"
  model = torch.hub.load(model_url, 'custom', path="best.pt", force_reload=True)
  return model


demo_img = "katarak1.png"
demo_video = "My Eyes.mp4"

st.title('Deteksi Mata Katarak')
st.sidebar.title('App Mode')


app_mode = st.sidebar.selectbox('Choose the App Mode',
                                ['About App','Run on Image','Run on Video','Run on WebCam'])

if app_mode == 'About App':
    st.subheader("PERHATIAN")
    st.markdown("<h5>INI ADALAH CONTOH FOTO JIKA UPLOAD GAMBAR</h5>",unsafe_allow_html=True)    
    st.markdown("- <h5>CONTOH 1</h5>",unsafe_allow_html=True)
    st.image("katarak1.png")
    st.markdown("- <h5>CONTOH 2</h5>",unsafe_allow_html=True)
    st.image("mata2.png")

if app_mode == 'Run on Image':
    st.subheader("Deteksi Mata Katarak:")
    text = st.markdown("")
    
    st.sidebar.markdown("---")
    # Input for Image
    img_file = st.sidebar.file_uploader("Upload an Image",type=["jpg","jpeg","png"])
    if img_file:
        image = np.array(Image.open(img_file))
    else:
        image = np.array(Image.open(demo_img))
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Original Image**")
    st.sidebar.image(image)
    
    # predict the image
    model = load_model()
    results = model(image)
    length = len(results.xyxy[0])
    output = np.squeeze(results.render())
    text.write(f"<h1 style='text-align: center; color:red;'>{length}</h1>",unsafe_allow_html = True)
    st.subheader("Output Image")
    st.image(output,use_column_width=True)
    
if app_mode == 'Run on Video':
    st.subheader("Deteksi Mata Katarak:")
    text = st.markdown("")
    
    st.sidebar.markdown("---")
    
    st.subheader("Output")
    stframe = st.empty()
    
    #Input for Video
    video_file = st.sidebar.file_uploader("Upload a Video",type=['mp4','mov','avi','asf','m4v'])
    st.sidebar.markdown("---")
    tffile = tempfile.NamedTemporaryFile(delete=False)
    
    if not video_file:
        vid = cv2.VideoCapture(demo_video)
        tffile.name = demo_video
    else:
        tffile.write(video_file.read())
        vid = cv2.VideoCapture(tffile.name)
    
    st.sidebar.markdown("**Input Video**")
    st.sidebar.video(tffile.name)
    
    # predict the video
    while vid.isOpened():
        ret, frame = vid.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        model = load_model()
        results = model(frame)
        length = len(results.xyxy[0])
        output = np.squeeze(results.render())
        text.write(f"<h1 style='text-align: center; color:red;'>{length}</h1>",unsafe_allow_html = True)
        stframe.image(output)
        
if app_mode == 'Run on WebCam':
    st.subheader("Deteksi Mata Katarak:")
    text = st.markdown("")
    
    st.sidebar.markdown("---")
    
    st.subheader("Output")
    stframe = st.empty()
    
    run = st.sidebar.button("Start")
    stop = st.sidebar.button("Stop")
    st.sidebar.markdown("---")
    
    cam = cv2.VideoCapture(0)
    if(run):
        while(True):
            if(stop):
                break
            ret,frame = cam.read()
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            model = load_model()
            results = model(frame)
            length = len(results.xyxy[0])
            output = np.squeeze(results.render())
            text.write(f"<h1 style='text-align: center; color:red;'>{length}</h1>",unsafe_allow_html = True)
            stframe.image(output)
