import streamlit as st
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import re
import string
import requests
from bs4 import BeautifulSoup

# Define thresholds for detecting AI-generated text and plagiarism
ai_generated_threshold = 80
ai_detection_threshold = 10
plagiarism_threshold = 10

# Function to generate a base64-encoded bar chart
def generate_bar_chart(ai_percentage, human_percentage):
    # Normalize the percentages to make sure they add up to 100%
    total_percentage = ai_percentage + human_percentage
    if total_percentage > 100:
        ai_percentage = (ai_percentage / total_percentage) * 100
        human_percentage = (human_percentage / total_percentage) * 100
    elif total_percentage < 100:
        human_percentage += (100 - total_percentage)

    fig, ax = plt.subplots()

    # Data for the bar chart
    categories = ['AI Generated', 'Human Generated']
    values = [ai_percentage, human_percentage]
    colors = ['#FF6347', '#4682B4']  # Red for AI, Blue for Human

    bars = ax.bar(categories, values, color=colors)
    ax.set_xlabel('Text Type')
    ax.set_ylabel('Percentage')
    ax.set_title('AI vs Human Generated Text')

    # Convert plot to image and encode as base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return image_base64

def fetch_wikipedia_article(query):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "srlimit": 1
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "query" in data and "search" in data["query"] and data["query"]["search"]:
            page = data["query"]["search"][0]
            page_id = page["pageid"]
            article_content = fetch_wikipedia_page_content(page_id)
            if article_content:
                return article_content, f"https://en.wikipedia.org/?curid={page_id}", page["title"]
            else:
                st.error("Error fetching Wikipedia article content.")
                return "", "", ""
        else:
            st.error("No related articles found on Wikipedia.")
            return "", "", ""
    except requests.RequestException as e:
        st.error(f"Error fetching data from Wikipedia API: {e}")
        return "", "", ""

def fetch_wikipedia_page_content(page_id):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "pageid": page_id,
        "format": "json",
        "prop": "text"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "parse" in data and "text" in data["parse"]:
            soup = BeautifulSoup(data["parse"]["text"]["*"], "html.parser")
            paragraphs = soup.find_all('p')
            page_content = " ".join([para.get_text() for para in paragraphs])
            return page_content
        else:
            st.error("Unexpected response format from Wikipedia API.")
            return ""
    except requests.RequestException as e:
        st.error(f"Error fetching page content from Wikipedia API: {e}")
        return ""

def calculate_ai_percentage(text):
    text = re.sub(f"[{string.punctuation}0-9]", "", text)
    words = text.lower().split()
    unique_words = set(words)
    unique_ratio = len(unique_words) / len(words)
    ai_percentage = (1 - unique_ratio) * 100
    return ai_percentage

def calculate_human_percentage(text):
    import random
    return random.uniform(60, 100)  # Example value for demonstration

def detect_plagiarism_and_ai_text(inputQuery, article_content, url):
    lowercaseQuery = inputQuery.lower()
    queryWordList = re.sub("[^\w]", " ", lowercaseQuery).split()
    databaseWordList = re.sub("[^\w]", " ", article_content.lower()).split()
    plagiarized_words = set(queryWordList) & set(databaseWordList)
    matchPercentage = (len(plagiarized_words) / len(queryWordList)) * 100

    plagiarism_status = ""
    if matchPercentage >= plagiarism_threshold:
        plagiarism_status = "Plagiarism Detected"
    elif matchPercentage > 0:
        plagiarism_status = "Limited Plagiarism"

    ai_percentage = calculate_ai_percentage(inputQuery)
    is_ai_text = ai_percentage > ai_generated_threshold
    ai_text_detected = ai_percentage > ai_detection_threshold
    human_percentage = calculate_human_percentage(inputQuery)

    return matchPercentage, plagiarism_status, ai_percentage, is_ai_text, ai_text_detected, human_percentage, plagiarized_words, url

def show():
    st.title('Plagiarism Checker Tool')

    st.markdown("""
        <h2 style='color: #FF6347;'>AI vs Human Generated Text</h2>
    """, unsafe_allow_html=True)

    st.write("""
    This tool checks for plagiarism and AI-generated text. Enter your text in the input box and click "Check".
    """)

    uploaded_file = st.file_uploader("Choose a file")
    input_text = ""
    if uploaded_file is not None:
        st.write("Uploaded file detected. Trying to read content...")

        # Try reading the file with different encodings
        encodings = ['utf-8', 'ISO-8859-1', 'latin1']
        for encoding in encodings:
            try:
                input_text = uploaded_file.read().decode(encoding)
                st.write(f"File successfully decoded with encoding: {encoding}")
                break  # Exit loop if decoding is successful
            except UnicodeDecodeError as e:
                st.write(f"Error decoding with encoding {encoding}: {e}")
                continue
        else:
            st.error("Unable to decode the file with available encodings.")
            return

    if uploaded_file is None:
        input_text = st.text_area("Or, enter your text here:", height=200)

    if input_text:
        if st.button("Check"):
            st.write("Fetching related article from Wikipedia...")

            query = " ".join(input_text.split()[:5])  # Use the first 5 words of the input as the query
            st.write(f"Query for Wikipedia search: {query}")
            article_content, url, title = fetch_wikipedia_article(query)
            
            if article_content:
                st.write("Article content fetched successfully.")
                matchPercentage, plagiarism_status, ai_percentage, is_ai_text, ai_text_detected, human_percentage, plagiarized_words, url = detect_plagiarism_and_ai_text(input_text, article_content, url)

                st.subheader("Analysis Results:")
                st.write(f"Plagiarism Match Percentage: {matchPercentage:.2f}%")
                st.write(f"AI Text Percentage: {ai_percentage:.2f}%")
                st.write(f"Human Text Percentage: {human_percentage:.2f}%")
                st.write(f"Plagiarism Status: {plagiarism_status}")

                if ai_text_detected:
                    st.write("AI Text Detected")
                else:
                    st.write("AI Text Not Detected")

                st.subheader("User Text:")
                st.markdown(input_text)

                st.subheader("Highlighted Plagiarized Content:")
                highlighted_text = input_text
                for word in plagiarized_words:
                    highlighted_text = re.sub(rf"\b({word})\b", f"[{word}]({url})", highlighted_text, flags=re.IGNORECASE)
                st.markdown(highlighted_text, unsafe_allow_html=True)

                # Display the chart based on AI and Human percentages
                chart_image_base64 = generate_bar_chart(ai_percentage, human_percentage)
                st.markdown(f"""
                    <img src="data:image/png;base64,{chart_image_base64}" style="max-width: 100%; height: auto;" />
                """, unsafe_allow_html=True)

            else:
                st.write("No related article found on Wikipedia or an error occurred.")
        else:
            st.write("Please enter text and click 'Check'.")

if __name__ == "__main__":
    show()
