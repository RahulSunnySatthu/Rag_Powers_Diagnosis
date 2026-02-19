# OCR logic
import pytesseract
from PIL import Image

# Optional: Set path to Tesseract executable (Windows only)
# Uncomment and modify if needed:
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\User\Downloads\tesseract-ocr-w64-setup-5.5.0.20241111.exe"

def extract_image_text(file_path: str) -> str:
    """
    Extracts text from an image using Tesseract OCR.
    Returns extracted text as a string.
    """
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text

    except Exception as e:
        raise Exception(f"OCR processing failed: {str(e)}")
