from io import BytesIO
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def convert_docx_to_pdf_in_memory(docx_buffer: BytesIO):
    # Read the DOCX file from the in-memory content
    document = Document(docx_buffer)
    
    # Create an in-memory bytes buffer for the PDF
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
    
    width, height = letter
    # pdf.setFont("Helvetica", 12)
    y_position = height - 40  # Start a bit below the top of the page

    for paragraph in document.paragraphs:
        text = paragraph.text
        pdf.drawString(40, y_position, text)
        y_position -= 15  # Move down the page for the next line

        if y_position < 40:  # If at the bottom of the page, create a new page
            pdf.showPage()
            y_position = height - 40

    pdf.save()
    
    # Get the PDF content from the buffer
    pdf_buffer.seek(0)
    return pdf_buffer
