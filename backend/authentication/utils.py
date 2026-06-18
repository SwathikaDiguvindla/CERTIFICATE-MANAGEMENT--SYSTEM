import os
import qrcode

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black
from reportlab.lib.units import inch

from django.conf import settings


def generate_certificate_pdf(certificate):

    # Create folders
    certificate_folder = os.path.join(
        settings.MEDIA_ROOT,
        "certificates"
    )

    qr_folder = os.path.join(
        settings.MEDIA_ROOT,
        "qr_codes"
    )

    os.makedirs(certificate_folder, exist_ok=True)
    os.makedirs(qr_folder, exist_ok=True)


    # PDF path
    pdf_filename = f"{certificate.certificate_id}.pdf"

    pdf_path = os.path.join(
        certificate_folder,
        pdf_filename
    )


    # ---------------- QR CODE ----------------

    qr_data = (
        f"http://127.0.0.1:8000/verify/"
        f"{certificate.certificate_id}"
    )


    qr = qrcode.make(qr_data)

    qr_path = os.path.join(
        qr_folder,
        f"{certificate.certificate_id}.png"
    )

    qr.save(qr_path)


    # Save QR path in database
    certificate.qr_code = qr_path


    # ---------------- PDF DESIGN ----------------

    c = canvas.Canvas(
        pdf_path,
        pagesize=A4
    )


    width, height = A4


    # Border
    c.setStrokeColor(
        HexColor("#1a3a5c")
    )

    c.setLineWidth(5)

    c.rect(
        40,
        40,
        width-80,
        height-80
    )


    # Title
    c.setFillColor(
        HexColor("#1a3a5c")
    )

    c.setFont(
        "Helvetica-Bold",
        28
    )

    c.drawCentredString(
        width/2,
        height-120,
        "CERTIFICATE OF COMPLETION"
    )


    # Subtitle

    c.setFillColor(black)

    c.setFont(
        "Helvetica",
        16
    )

    c.drawCentredString(
        width/2,
        height-170,
        "This certificate is proudly presented to"
    )


    # Student Name

    c.setFont(
        "Helvetica-Bold",
        24
    )

    c.drawCentredString(
        width/2,
        height-230,
        certificate.name
    )


    # Details

    c.setFont(
        "Helvetica",
        14
    )


    c.drawCentredString(
        width/2,
        height-290,
        f"Domain : {certificate.domain}"
    )


    c.drawCentredString(
        width/2,
        height-320,
        f"Duration : {certificate.start_date} to {certificate.end_date}"
    )


    c.drawCentredString(
        width/2,
        height-350,
        f"Certificate ID : {certificate.certificate_id}"
    )


    # QR IMAGE

    c.drawImage(
        qr_path,
        width-170,
        80,
        100,
        100
    )


    # Footer

    c.setFont(
        "Helvetica-Oblique",
        12
    )

    c.drawCentredString(
        width/2,
        80,
        "CV Portal Certificate Management System"
    )


    c.save()


    return pdf_path