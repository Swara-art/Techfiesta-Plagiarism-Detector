from pdf2image import convert_from_path
import pytesseract
import os

# CHANGE THIS to the absolute path of a SCANNED PDF
PDF_PATH = r"D:\Git+Handbook.pdf"

# CHANGE THIS only if Poppler is NOT in PATH
# If poppler IS in PATH, you can delete this variable entirely
POPPLER_PATH = r"C:\poppler\poppler-25.12.0\Library\bin"


def main():
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"PDF not found at: {PDF_PATH}")

    print("📄 Reading PDF:", PDF_PATH)

    images = convert_from_path(
        PDF_PATH,
        poppler_path=POPPLER_PATH  # remove this line if poppler is in PATH
    )

    print(f"🖼 Pages detected: {len(images)}")

    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img)
        print(f"\n--- PAGE {i + 1} OCR OUTPUT ---")
        print(text[:1000])  # print first 1000 chars


if __name__ == "__main__":
    main()
