from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.utils import ImageReader
from django.conf import settings
import os


def generate_certificate_pdf(certificate):

    folder = os.path.join(settings.MEDIA_ROOT, "certificates")

    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = os.path.join(
        folder,
        f"{certificate.certificate_id}.pdf"
    )


    c = canvas.Canvas(
        file_path,
        pagesize=landscape(A4)
    )


    width, height = landscape(A4)


    # Background
    c.setFillColor(HexColor("#EAF6FF"))
    c.rect(0, 0, width, height, fill=1)


    # Outer border
    c.setStrokeColor(HexColor("#1A3A5C"))
    c.setLineWidth(8)
    c.rect(25, 25, width-50, height-50)


    # Title
    c.setFillColor(HexColor("#1A3A5C"))
    c.setFont("Helvetica-Bold", 35)

    c.drawCentredString(
        width/2,
        height-100,
        "CERTIFICATE OF COMPLETION"
    )


    # Subtitle
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 18)

    c.drawCentredString(
        width/2,
        height-150,
        "This certificate is proudly presented to"
    )


    # Student name
    c.setFillColor(HexColor("#D35400"))
    c.setFont("Helvetica-Bold", 32)

    c.drawCentredString(
        width/2,
        height-210,
        certificate.name.upper()
    )


    # Details
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 16)


    c.drawCentredString(
        width/2,
        height-270,
        f"Domain : {certificate.domain}"
    )


    c.drawCentredString(
        width/2,
        height-310,
        f"Duration : {certificate.start_date} to {certificate.end_date}"
    )


    # Certificate ID
    c.setFillColor(HexColor("#1A3A5C"))
    c.setFont("Helvetica-Bold", 14)

    c.drawString(
        80,
        80,
        f"Certificate ID : {certificate.certificate_id}"
    )


    # Footer
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 12)

    c.drawCentredString(
        width/2,
        60,
        "CV Portal Certificate Management System"
    )


    c.save()


    return file_path