from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.conf import settings
import os
import textwrap

def generate_pdf(note):
    pdf_dir = os.path.join(settings.MEDIA_ROOT, "pdfs")
    os.makedirs(pdf_dir, exist_ok=True)

    filename = f"note_{note.id}.pdf"
    pdf_path = os.path.join(pdf_dir, filename)

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    text = c.beginText(40, height - 50)
    text.setFont("Helvetica", 11)

    wrapped_lines = []
    for line in note.ocr_text.split("\n"):
        wrapped_lines.extend(textwrap.wrap(line, 90) or [""])

    for line in wrapped_lines:
        if text.getY() < 50:
            c.drawText(text)
            c.showPage()
            text = c.beginText(40, height - 50)
            text.setFont("Helvetica", 11)

        text.textLine(line)

    c.drawText(text)
    c.save()

    return f"pdfs/{filename}"
