from io import BytesIO
from docx import Document

def convert_docx_to_string(docx_buffer: BytesIO) -> str:
    # Read the DOCX file from the in-memory content
    document = Document(docx_buffer)
    
    # Create an empty string to store the content
    content = ""
    
    for paragraph in document.paragraphs:
        text = paragraph.text
        content += text + "\n"  # Add the paragraph text to the content string

    return content
