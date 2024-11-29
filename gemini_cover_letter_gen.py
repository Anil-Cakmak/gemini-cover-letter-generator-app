import streamlit as st
from helpers import *

col1, col2 = st.columns([1, 6])
with col1:
    st.image("gemini_generated_image.jpg", width=1000)
with col2:
    st.markdown("""
        <div style="display: flex; align-items: center; height: 100%;">
            <h1 style="font-size: 32px; margin: 0;">Super AI-Driven Cover Letter Builder</h1>
        </div>
    """, unsafe_allow_html=True)

st.write("""Welcome to the Super AI-Driven Cover Letter Builder! 
         Powered by Google Gemini 1.5 Flash, this tool helps you craft personalized, professional cover letters in just a few clicks. 
         Simply submit your details below, and let the app generate your cover letter. After creating your cover letter, you can download it in PDF or DOCX format.
         You can also refine it further using [this guide](https://capd.mit.edu/resources/how-to-write-an-effective-cover-letter/) for an even more tailored result.""")

st.write("""
To use this app, you need a Gemini API key. Please follow the steps below if you don't have one:

1. [Get a Gemini API key in Google AI Studio](https://aistudio.google.com/app/apikey?_gl=1*1elzb2j*_ga*Nzg0MDg5MzQ5LjE3MzIwNDcxOTk.*_ga_P1DBVKWT6V*MTczMjM1ODk3Ny4xOS4xLjE3MzIzNTk1MDguMjQuMC4xMzEwOTE1NTgy).
2. Follow the instructions to generate your API key.
3. Once you have your API key, come back to this app and enter it below.
""")

st.markdown(
    "<h1 style='color:red; text-transform: uppercase; font-size: 20px; '>Do not submit sensitive, confidential, or personal information!</h1>",
    unsafe_allow_html=True
)
st.write("Submit the details below to receive a custom, professional cover letter.")

job_title = st.text_input("Enter the job title *")
company_name = st.text_input("Enter the company name *")
recipient_name = st.text_input("Enter the recipient's name")
job_description = st.text_area("Enter the job description *")
platform = st.text_input("Platform where you saw the advertisement")
cv = uploaded_file = st.file_uploader("""Upload your CV in PDF format *     
                                      (REMOVE OR MASK ANY PERSONAL INFORMATION FROM YOUR CV BEFORE UPLOADING!)""", type="pdf")

if cv is not None:
    st.success("File uploaded successfully!")


gemini_api_key = st.text_input("Enter your Gemini API Key:", type="password")

if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "file_format" not in st.session_state:
    st.session_state.file_format = "PDF"

if st.button("Generate Cover Letter"):
    if not job_title or not company_name or not job_description or not cv or not gemini_api_key:
        st.warning("Please fill in all required fields before generating a cover letter.")
    else:
        with st.spinner("Generating your cover letter..."):
            try:
                configure(gemini_api_key)
                prompt = prompt(job_title, company_name, job_description, platform, recipient_name)
                response = generator(cv, prompt)

                st.session_state.generated_text = response

            except Exception as e:
                st.error(f"Error generating cover letter: {e}")

if not st.session_state.generated_text == "":
    try:
        st.subheader("Generated Cover Letter")
        st.text(st.session_state.generated_text)

        col1, col2, col3 = st.columns([3, 3, 2])
        with col2:  
            # Radio button to choose file format
            st.subheader("Download")
            file_format = st.radio("Choose a file format to download:", ["PDF", "DOCX"], horizontal=True)
            st.session_state.file_format = file_format

            # Create the file based on the selected format
            if st.session_state.file_format == "DOCX":
                file_data = cover_letter_docx(st.session_state.generated_text)
                file_name = "Firstname_Lastname_CoverLetter.docx"
                mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            elif st.session_state.file_format == "PDF":
                file_data = cover_letter_pdf(st.session_state.generated_text)
                file_name = "Firstname_Lastname_CoverLetter.pdf"
                mime_type = "application/pdf"

            # Show download button
            st.download_button(
                label="Download",
                data=file_data,
                file_name=file_name,
                mime=mime_type,
            )
            
    except Exception as e:
            st.error(f"Error: {e}")
