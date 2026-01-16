from pypdf import PdfReader

def read_txt(file) -> str:
    return file.file.read().decode("utf-8")

def read_pdf(file) -> str:
    reader = PdfReader(file.file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text(file) -> str:
    if file.filename.endswith(".txt"):
        return read_txt(file)
    elif file.filename.endswith(".pdf"):
        return read_pdf(file)
    else:
        raise ValueError("Formato de arquivo não suportado")