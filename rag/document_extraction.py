import fitz

def extract_pdf_text(file):
    document = fitz.open(stream=file, filetype="pdf")

    text = ""

    for page in document:
        text += page.get_text() + "\n"

    document.close()

    return text