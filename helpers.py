import google.generativeai as genai
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from io import BytesIO


def configure(gemini_api_key):
    genai.configure(api_key=gemini_api_key)


def prompt(job_title, company_name, job_description, platform, recipient_name="Hiring Manager"):
    return f"""This is a canditate's CV in pdf format. Extract the text considering layouts, headings and subheadings.
Then write a professional cover letter of 250-330 words based on this CV and the following details:
- Job Title: {job_title}
- Company: {company_name}
- Recipient’s Name: {recipient_name}
- Job Description: {job_description}
- Platform of the Advertisement: {platform}

Please ensure the cover letter is tailored to the specific role and company. It should:
1. Clearly state the purpose of the letter and introduce the candidate.
2. Demonstrate genuine interest in the job and company.
3. Complement the CV by offering a little more detail about key experiences, not to simply repeat the CV in paragraph form.
4. Focus on transferable skills if no direct experience exists.
5. Maintain a professional tone, be concise, and thank the reader for their time and consideration.

Structure:
- Introduction: State why the candidate is interested in the role and company.
- Body: Provide 2-3 key examples from the CV that show how the candidate's skills and experience align with the role.
- Closing: Reaffirm the candidate's interest and gratitude for the opportunity.

Be sure to personalize the letter and avoid generic language. The body paragraphs must be equal in size.
"""


def generator(cv, prompt):

    cv = genai.upload_file(cv, mime_type="application/pdf")
    version = 'models/gemini-1.5-flash'
    model = genai.GenerativeModel(version, generation_config={"temperature": 1.5, 
                                                            "top_p": 0.96, 
                                                            "max_output_tokens": 600})
    response = model.generate_content([cv, prompt])
    cv.delete()
    return response.text


def cover_letter_pdf(text):

    # Set up the canvas and page properties
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    width, height = A4
    c.setFont("Times-Roman", 12)

    # Margins
    margin = 72  # 1 inch = 72 points
    text_width = width - 2 * margin

    # Start position
    x, y = margin, height - margin

    # Line spacing
    line_height = 14  # Single-spaced lines, font size 12 + 2pt padding

    # Process text
    paragraphs = text.split("\n\n")
    for i, paragraph in enumerate(paragraphs):
        if i > 0:
            y -= line_height
        lines = c.beginText(x, y)
        wrapped_lines = simpleSplit(paragraph, "Times-Roman", 12, text_width)
        for line in wrapped_lines:
            lines.textLine(line)
            y -= line_height
        c.drawText(lines)

    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer


def cover_letter_docx(text):
    doc = Document()
    section = doc.sections[0]
    
    # Set A4 dimensions: 21.0 x 29.7 cm (8.27 x 11.69 inches)
    section.page_height = Inches(11.69)
    section.page_width = Inches(8.27)
    
    # Set one-inch margins
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    
    # Set default paragraph formatting
    style = doc.styles['Normal']
    style.paragraph_format.space_after = Pt(14)
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.line_spacing = Pt(14)
    style.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)

    # Split text into paragraphs and add to the document
    paragraphs = text.split("\n\n")
    for i, para in enumerate(paragraphs):
        if para.strip():
            paragraph = doc.add_paragraph(para.strip())
            
            # Set space after for all but the last paragraph
            if i == len(paragraphs) - 1:
                paragraph.paragraph_format.space_after = Pt(0)

    # Save document to buffer
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
