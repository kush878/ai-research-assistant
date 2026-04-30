from PyPDF2 import PdfReader

def load_pdf(file):
    text = ""
    reader = PdfReader(file)
    
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            # 🔥 CLEAN TEXT
            page_text = page_text.replace("\n", " ")
            page_text = page_text.replace("  ", " ")
            text += page_text + " "
    
    return text