import streamlit as st
import spacy
import fitz  
import docx  
import os

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to identify and classify entities
def identify_entities(text):
    doc = nlp(text)
    entities = [(entity.text, entity.label_) for entity in doc.ents]
    return entities

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

# Save uploaded file to local machine
def save_uploaded_file(uploaded_file):
    file_path = os.path.join("uploaded_files", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Save entities to a local file
def save_entities_to_file(entities, filename="entities.txt"):
    with open(filename, "w") as file:
        for entity, label in entities:
            file.write(f"Entity: {entity}, Label: {label}\n")

# Create directory for uploaded files if not exists
if not os.path.exists("uploaded_files"):
    os.makedirs("uploaded_files")

# Streamlit UI
st.title("Entity Recognition with spaCy")
st.header("Developed by Irfan")
st.write("Enter the text you want to analyze or upload a file:")

# Text input from user
input_text = st.text_area("Input Text", "")

# File uploader for text, DOCX, and PDF files
uploaded_file = st.file_uploader("Upload a text file, DOCX, or PDF", type=["txt", "docx", "pdf"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1]
    try:
        if file_extension == 'txt':
            input_text = uploaded_file.read().decode("utf-8")
        elif file_extension == 'pdf':
            input_text = extract_text_from_pdf(uploaded_file)
        elif file_extension == 'docx':
            input_text = extract_text_from_docx(uploaded_file)
        else:
            st.write("Unsupported file format. Please upload a text file (.txt), DOCX document (.docx), or PDF document (.pdf).")
        # Save the uploaded file locally
        save_uploaded_file(uploaded_file)
    except Exception as e:
        st.write(f"Error processing file: {e}")

if input_text:
    st.text_area("Input Text", value=input_text, height=250)

if st.button("Identify Entities"):
    if input_text.strip() != "":
        try:
            entities = identify_entities(input_text)
            
            if entities:
                st.write("Entities found in the text:")
                for entity, label in entities:
                    st.write(f"Entity: {entity}, Label: {label}")
                # Save entities to file
                save_entities_to_file(entities)
                st.write("Entities have been saved to 'entities.txt' in the local directory.")
            else:
                st.write("No entities found.")
        except Exception as e:
            st.write(f"Error: {e}")
    else:
        st.write("Please enter some text or upload a file to analyze.")
