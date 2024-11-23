from helpers import *
import streamlit as st

st.title("Cover Letter Generator")

st.markdown(
    "<h1 style='color:red; text-transform: uppercase; font-size: 20px; '>Do not submit sensitive, confidential, or personal information!</h1>",
    unsafe_allow_html=True
)
st.write("Fill in the details below to generate a customized, professional cover letter.")

job_title = st.text_input("Enter job title *")
company_name = st.text_input("Enter company name *")
job_description = st.text_area("Enter your job description *")
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