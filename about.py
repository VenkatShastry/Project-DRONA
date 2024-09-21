import streamlit as st

def show():
    st.title("About DRONA")

    st.write("""
    **Welcome to DRONA: Sharpening Your Professional Edge!**

    DRONA is an innovative tool designed to enhance your professional documents and improve your chances of career success. Our project comprises two main modules: the Plagiarism Tool and the Resume ATS Guide. Both modules aim to provide users with detailed insights and feedback, helping them to present their best selves in their professional endeavors.

    ### Plagiarism Tool
    Our Plagiarism Tool allows users to upload documents or text for comprehensive analysis. The tool detects human-generated and AI-generated content while highlighting any instances of plagiarism. Users receive clear, actionable feedback, with plagiarized sections marked and linked to the original content on Wikipedia, ensuring proper attribution and originality.

    ### Resume ATS Guide
    The Resume ATS Guide assists users in optimizing their resumes to pass through Applicant Tracking Systems (ATS) used by many employers today. Users can upload their resumes and job descriptions for a detailed analysis. The guide leverages the Gemini API to provide personalized feedback, suggesting improvements and offering career recommendations based on the content of the resume. Additionally, it evaluates the likelihood of job application success by comparing the resume against job descriptions.

    ### Key Features
    - **User Document Input:** Seamlessly upload documents or text for analysis.
    - **Plagiarism Detection:** Identify human-generated, AI-generated content, and instances of plagiarism.
    - **Highlighting Plagiarism:** Highlight plagiarized sections with links to original sources.
    - **Job Description Input:** Upload job descriptions for tailored analysis and feedback.
    - **Resume Analysis:** Utilize the Gemini API for in-depth resume analysis and feedback.
    - **Career Recommendations:** Receive career suggestions based on resume content.
    - **Success Assessment:** Evaluate the likelihood of job application success through resume and job description comparison.
    - **User Registration and Login:** Secure user authentication and data management using PostgreSQL.

    ### Technologies Used
    DRONA leverages several advanced technologies to deliver its functionalities:
    - **Streamlit:** For building the web interface.
    - **Python:** The core programming language used for backend development.
    - **OpenAI:** For AI-driven analysis and content generation.
    - **Gemini API:** For resume analysis and career recommendations.
    - **BeautifulSoup and Requests:** For web scraping and handling HTTP requests.
    - **PIL and pdf2Image:** For processing and converting PDF files.
    - **Base64:** For secure data encoding.
    - **PostgreSQL:** For user registration and login management.
    - **CSS and JavaScript:** For frontend design and interactivity.

    ### Our Mission
    At DRONA, our mission is to empower professionals by providing them with the tools they need to stand out in today's competitive job market. We strive to offer reliable, accurate, and insightful feedback to help users enhance their professional documents and increase their chances of career success.

    We hope you find DRONA valuable in your professional journey. Thank you for choosing our tool to sharpen your edge!

    For more information, support, or feedback, please contact us at +91-8105600220.
    """)
