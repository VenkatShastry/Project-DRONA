import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai
import apikey as ap

# Set your API key
my_api_key = ap.GOOGLE_API_KEY
genai.configure(api_key=my_api_key)

def get_gemini_response(input_text, pdf_content, prompt):
    """Fetches response from Gemini model using provided API key."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])

    return response.text

def input_pdf_setup(uploaded_file):
    """Converts the uploaded PDF to image data."""
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {"mime_type": "image/jpeg", "data": base64.b64encode(img_byte_arr).decode()}
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")

def show(): 
    st.header("DRONA's ATS Resume Tool")

    input_text = st.text_area("Enter the Job Description here", key="input")
    uploaded_file = st.file_uploader("Upload your Resume here (PDF).. !", type=["pdf"])

    if uploaded_file is not None:
        st.write("File Uploaded Successfully")

    submit1 = st.button("Tell me About the Resume")
    submit2 = st.button("Identify my best career fit.")
    submit3 = st.button("Percentage Match")

    input_prompt1 = """
    You are a highly experienced Human Resource Manager and Technical Interview Expert. Your task is to review the resume uploaded by the user. Please:

    Summarize the user's educational background briefly.
    Highlight the user's technical and non-technical skills.
    Based on the listed skills, provide guidance on which additional skills or technologies the user should learn.
    Suggest the most suitable career path for the user.
    If the resume includes any projects, offer your expert suggestions on them.
    If there is work experience listed, analyze the roles and provide career advice accordingly.
    Please ensure your feedback is concise and to the point, with clear spacing between each section.
    """

    input_prompt3 = """
    You are a skilled ATS (Applicant Tracking System) scanner with expertise in data science and ATS functionality. Your task is to evaluate the resume against the provided job description. Please:

    Provide the match percentage between the resume and the job description.
    List the missing keywords, focusing on the most important ones (up to 10 keywords). If there are more than 10, mention 'these are the Trending ones but you can learn others like ...' and list them separated by commas.
    Offer final thoughts on the resume in relation to the job description.
    Ensure that each part of your response is clearly separated by spaces or displayed on the next lines. Make sure to Highlight the Section with headings.
    """

    input_prompt2 = """
    You are a skilled ATS (Applicant Tracking System) scanner with expertise in data science and ATS functionality. Evaluate the resume and identify the best-suited job roles based on the included skills. Please:

    Begin with 'Your resume has...' and list the key skills. Don't include all, only which are top skills.
    Recommend suitable job roles and explain why. Don't make it too lengthy.
    Suggest additional skills or technologies to learn if necessary. Max of 7.
    Provide the average salary for each role. Make sure to give spaces after each role. and don't include more than 5.
    Estimate the percentage chance of selection for each role. and highlight this.
    Ensure clarity and brevity in your response.

    Don't use other styles like italic or anything to highlight, just make it bold if you want to highlight.
    Make sure it should not be too long, and easily understood by the user.
    """

    if submit1:
        st.header("Unleashing the Knowledge of DRONA...")
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt1)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.write("Please upload the resume")

    elif submit3:
        st.header("Unleashing the Knowledge of DRONA...")
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt3)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.write("Please upload the resume")

    elif submit2:
        st.header("Unleashing the Knowledge of DRONA...")
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt2)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.write("Please upload the resume")

if __name__ == "__main__":
    show()
