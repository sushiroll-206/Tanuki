import pdfplumber

def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = " ".join(page.extract_text() for page in pdf.pages if page.extract_text())
    return text