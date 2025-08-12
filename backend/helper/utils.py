import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text


def chunk_text(text, max_length=500):
    chunks = []
    words = text.split()
    chunk = []
    for word in words:
        if len(" ".join(chunk + [word])) <= max_length:
            chunk.append(word)
        else:
            chunks.append(" ".join(chunk))
            chunk = [word]
    if chunk:
        chunks.append(" ".join(chunk))
    return chunks
