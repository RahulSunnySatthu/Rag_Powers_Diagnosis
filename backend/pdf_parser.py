# PDF parsing logic
import pdfplumber

def extract_pdf_text(file_path: str) -> str:
    """
    Extracts text from a PDF file using pdfplumber.
    Returns full extracted text as a string.
    """
    full_text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    return full_text
