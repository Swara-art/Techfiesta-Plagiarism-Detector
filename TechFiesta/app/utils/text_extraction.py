from fastapi import HTTPException
from io import BytesIO
import pdfplumber
from pathlib import Path

MIN_TEXT_LENGTH = 50


def extract_text_from_bytes(filename: str, file_bytes: bytes) -> str:
    """
    Entry point for all text extraction.
    Works with TXT, digital PDF, and scanned PDF (OCR).
    """
    filename = filename.lower()

    if filename.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore").strip()

    if filename.endswith(".pdf"):
        text = _extract_pdf_text(file_bytes)

        if len(text.strip()) < MIN_TEXT_LENGTH:
            print("⚠️ Low text detected → running OCR")
            text = _extract_pdf_text_ocr(file_bytes)

        return text.strip()

    raise HTTPException(status_code=415, detail="Unsupported file type")


def _extract_pdf_text(file_bytes: bytes) -> str:
    """Extract text from digital PDFs"""
    text_chunks = []

    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)

    return "\n".join(text_chunks)


def _extract_pdf_text_ocr(file_bytes: bytes) -> str:
    """OCR fallback for scanned PDFs"""
    try:
        from pdf2image import convert_from_bytes
        import pytesseract

        images = convert_from_bytes(file_bytes)
        print(f"🖼 OCR pages detected: {len(images)}")

        ocr_text = []
        for i, img in enumerate(images):
            text = pytesseract.image_to_string(img, config="--psm 6")
            print(f"📄 OCR page {i} text length: {len(text)}")
            if text.strip():
                ocr_text.append(text)

        return "\n".join(ocr_text)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OCR failed: {e}")

def extract_text_from_file(file_path: Path) -> str:
    suffix = file_path.suffix.lower()

    if suffix == ".txt":
        return file_path.read_text(encoding="utf-8", errors="ignore")

    if suffix == ".pdf":
        text = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        return "\n".join(text)

    raise ValueError(f"Unsupported file type: {suffix}")