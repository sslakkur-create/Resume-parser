import re
from pdfminer.high_level import extract_text as pdf_extract
from docx import Document


def extract_text_from_pdf(file) -> str:
    return pdf_extract(file)


def extract_text_from_docx(file) -> str:
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])


def extract_text(file, filename: str) -> str:
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(file)
    else:
        return file.read().decode("utf-8", errors="ignore")


def clean_text(text: str) -> str:
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()
