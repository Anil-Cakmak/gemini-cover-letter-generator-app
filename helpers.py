import google.generativeai as genai

def configure(gemini_api_key):
    genai.configure(api_key=gemini_api_key)


def prompt(job_title, company_name, job_description):
    return f"""This is a canditate's CV in the pdf format. Extract the text considering layouts, headings and subheadings.
Then write a professional cover letter of 250-400 words based on this CV and the following details:

- Job Title: {job_title}
- Company: {company_name}
- Job Description: {job_description}

Please ensure the cover letter is tailored to the specific role and company. It should:
1. Clearly state the purpose of the letter and introduce the candidate.
2. Demonstrate genuine interest in the job and company.
3. Highlight relevant skills and experiences with brief, specific examples from the CV.
Try not to simply repeat the CV in paragraph form, complement the CV by offering a little more detail about key experiences.
4. Focus on transferable skills if no direct experience exists.
5. Maintain a professional tone, be concise (one page), and thank the reader for their time and consideration.

Structure:
- Introduction: State why the candidate is interested in the role and company.
- Body (2-3 paragraphs of similar sizes): Provide 2-3 key examples from the CV that show how the candidate's skills and experience align with the role.
- Closing: Reaffirm the candidate's interest and gratitude for the opportunity.

Be sure to personalize the letter and avoid generic language. Also do not simply repeat the CV in paragraph form, complement the CV by offering a little more detail about key experiences.
"""


def generator(cv, prompt):
    cv = genai.upload_file(cv, mime_type="application/pdf")
    version = 'models/gemini-1.5-flash'
    model = genai.GenerativeModel(version, generation_config={"temperature": 1.5, 
                                                            "top_p": 0.97, 
                                                            "max_output_tokens": 700})
    response = model.generate_content([cv, prompt])
    cv.delete()
    return response.text