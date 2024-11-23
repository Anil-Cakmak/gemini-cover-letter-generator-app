from helpers import *
import streamlit as st

st.title("AI-Driven Cover Letter Builder")

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
job_description = st.text_area("Enter the job description *")
cv = uploaded_file = st.file_uploader("""Upload your CV in PDF format *     (REMOVE OR MASK ANY PERSONAL INFORMATION FROM YOUR CV BEFORE UPLOADING!)""",
                                        type="pdf")

if cv is not None:
    st.success("File uploaded successfully!")


gemini_api_key = st.text_input("Enter your Gemini API Key:", type="password")

if st.button("Generate Cover Letter"):
    if not job_title or not company_name or not job_description or not cv or not gemini_api_key:
        st.warning("Please fill in all fields before generating a cover letter.")
    else:
        with st.spinner("Generating your cover letter..."):
            try:       
                configure(gemini_api_key)
                prompt = prompt(job_title, company_name, job_description)
                response = generator(cv, prompt)              
                
                st.subheader("Generated Cover Letter")
                st.write(response)
            except Exception as e:
                st.error(f"Error generating cover letter: {e}")