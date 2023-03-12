import streamlit as st
import AnswerScoring as asc
import numpy as np
import cv2
from PIL import Image
# Set the name of the app as the title
st.set_page_config(page_title='IntelliCheck App')

menu = ["Home","Upload Q&A","Check Student's answer"]
choice = st.sidebar.selectbox("Menu",menu)

if choice == "Home":
     # Display the app name as a header
     st.markdown("<h1 style='text-align: center;'>IntelliCheck App</h1>", unsafe_allow_html=True)
     # Display the one-line description below the header in a smaller font size
     st.markdown("<h4 style='text-align: center;'>Revolutionize grading with OCR technology that categorizes student mistakes in seconds</h4>", unsafe_allow_html=True)

if choice == "Upload Q&A":
    st.subheader("Enter Question Number,answer key")
    with st.form(key='form1'):
        question = st.text_input("Question Number")
        num = int(st.number_input("Enter the the number of marks allotted to this question",step = 1,min_value=0,max_value=100))
        submit_button = st.form_submit_button(label='Enter the answer key')
        x=[""]*num
        for i in range(num):
               st.session_state[i] = st.text_input(f"Enter the keywords for point {i+1}")
               x.append(st.session_state[i])
        st.session_state["list_of_points"] = x
        submit_button = st.form_submit_button(label='Submit Answer key!')

    if(submit_button):
       
       st.success("Sample Answer Key submitted succesfully!")
if choice == "Check Student's answer":
     st.subheader("OCR Answer Checking")
     
     uploaded_file = st.file_uploader("Please upload an image")
     if uploaded_file is not None:
    # Convert the file to an opencv image.
       file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
       image = cv2.imdecode(file_bytes, 1)
     st.image(image)
     
     submit_button = st.button("Submit Answer and Assign marks!")
     if(submit_button):
               result = asc.check_answer(st.session_state["list_of_points"],  image)
               st.success("This answer gets: "+ str(result[0]) +" \nThe errors are: "+result[1])

          