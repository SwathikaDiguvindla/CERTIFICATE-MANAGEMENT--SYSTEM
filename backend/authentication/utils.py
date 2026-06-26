import os
import qrcode
from datetime import datetime

from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader


def generate_certificate_pdf(certificate):

    certificate_dir = os.path.join(settings.MEDIA_ROOT, "certificates")
    os.makedirs(certificate_dir, exist_ok=True)

    pdf_path = os.path.join(
        certificate_dir,
        f"{certificate.certificate_id}.pdf"
    )

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    template = os.path.join(
        settings.BASE_DIR,
        "authentication",
        "static",
        "certificate_template.png"
    )

    c.drawImage(
        ImageReader(template),
        0,
        0,
        width=width,
        height=height
    )

    if isinstance(certificate.start_date, str):
        start_date = datetime.strptime(certificate.start_date, "%Y-%m-%d")
    else:
        start_date = certificate.start_date

    if isinstance(certificate.end_date, str):
        end_date = datetime.strptime(certificate.end_date, "%Y-%m-%d")
    else:
        end_date = certificate.end_date

    start = start_date.strftime("%d %B %Y")
    end = end_date.strftime("%d %B %Y")
    today = datetime.today().strftime("%d %B %Y")

    # Date
    c.setFont("Times-Bold", 12)
    c.drawString(450, 662, today)

# Student Name
    c.setFont("Times-Bold", 14)
    c.drawString(300, 592, certificate.name)

# Domain
    c.setFont("Times-Bold", 13)
    c.drawString(387, 548, certificate.domain)

# Start Date
    c.setFont("Times-Bold", 11)
    c.drawString(315, 502, start)

# End Date
    c.drawString(443, 502, end)

# Certificate ID
    c.setFont("Helvetica-Bold", 9)
    c.drawString(145, 19, certificate.certificate_id)




    # QR Code
    qr_data = (
        f"Certificate ID: {certificate.certificate_id}\n"
        f"Name: {certificate.name}\n"
        f"Domain: {certificate.domain}\n"
        f"Duration: {start} to {end}"
    )

    qr = qrcode.make(qr_data)
    qr_path = os.path.join(
        certificate_dir,
        f"{certificate.certificate_id}_qr.png"
    )
    qr.save(qr_path)

    c.drawImage(
        qr_path,
        365,
        55,
        width=65,
        height=65
    )

    c.save()
    return pdf_path