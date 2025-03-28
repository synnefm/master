import os
import glob
import PyPDF2
from pdf2image import convert_from_path
import pytesseract

DATA_FOLDER = "../../Data/Journaler"

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF using PyPDF2."""
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def ocr_pdf_with_tesseract(pdf_path, dpi=300, lang='nor'):
    """Convert PDF pages to images and run OCR on each page using Tesseract."""
    images = convert_from_path(pdf_path, dpi=dpi)
    ocr_text = ""
    for i, image in enumerate(images):
        page_text = pytesseract.image_to_string(image, lang=lang)
        ocr_text += f"--- Page {i+1} ---\n" + page_text + "\n"
    return ocr_text

def main():
    # Build the search path for PDF files in the data folder
    pdf_search_pattern = os.path.join(DATA_FOLDER, "*.pdf")
    pdf_files = glob.glob(pdf_search_pattern)
    
    if not pdf_files:
        print("No PDF files found in the data folder.")
        return

    pdf_path = pdf_files[0]
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # 1. Extract text using PDF extraction
    extracted_text = extract_text_from_pdf(pdf_path)
    extraction_txt_file = os.path.join(DATA_FOLDER, f"{base_name}_extracted.txt")
    with open(extraction_txt_file, 'w', encoding='utf-8') as f:
        f.write(extracted_text)
    print(f"Extracted text written to {extraction_txt_file}")
    
    # 2. Extract text using OCR via Tesseract
    ocr_text = ocr_pdf_with_tesseract(pdf_path)
    ocr_txt_file = os.path.join(DATA_FOLDER, f"{base_name}_ocr.txt")
    with open(ocr_txt_file, 'w', encoding='utf-8') as f:
        f.write(ocr_text)
    print(f"OCR text written to {ocr_txt_file}")

if __name__ == "__main__":
    main()
