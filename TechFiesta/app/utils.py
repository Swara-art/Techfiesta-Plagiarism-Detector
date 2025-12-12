import PyPDF2
import docx
from fastapi import HTTPException
import io


def extract_text_from_pdf(file_stream: io.BytesIO) -> str:
    """Extracts text from a PDF file stream."""
    try:
        pdf_reader = PyPDF2.PdfReader(file_stream)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        raise HTTPException(status_code=400, detail=f"Error processing PDF file: {str(e)}")

def extract_text_from_docx(file_stream: io.BytesIO) -> str:
    """Extracts text from a DOCX file stream."""
    try:
        document = docx.Document(file_stream)
        text = ""
        for para in document.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        raise HTTPException(status_code=400, detail=f"Error processing DOCX file: {str(e)}")

def extract_text_from_txt(file_stream: io.BytesIO) -> str:
    """Extracts text from a TXT file stream."""
    try:
        text = file_stream.read().decode('utf-8', errors='ignore')
        return text
    except Exception as e:
        print(f"Error reading TXT: {e}")
        raise HTTPException(status_code=400, detail=f"Error processing TXT file: {str(e)}")
    
def extract_text_from_plain(file_stream: io.BytesIO) -> str:
    """Try reading any file as plain text."""
    try:
        return file_stream.read().decode("utf-8", errors="ignore")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Cannot read file as text: {e}")
