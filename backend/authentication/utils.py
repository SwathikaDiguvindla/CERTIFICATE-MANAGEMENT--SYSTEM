import os
import qrcode

from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas


def generate_certificate_pdf(certificate):

    certificate_dir = os.path.join(
        settings.MEDIA_ROOT,
        "certificates"
    )

    os.makedirs(certificate_dir, exist_ok=True)

    pdf_path = os.path.join(
        certificate_dir,
        f"{certificate.certificate_id}.pdf"
    )

    c = canvas.Canvas(
        pdf_path,
        pagesize=landscape(A4)
    )

    width, height = landscape(A4)

    # ==========================================
    # BACKGROUND
    # ==========================================

    c.setFillColor(colors.whitesmoke)
    c.rect(0, 0, width, height, fill=1)

    # ==========================================
    # BORDERS
    # ==========================================

    c.setStrokeColor(colors.HexColor("#C9A227"))
    c.setLineWidth(5)
    c.rect(
        20,
        20,
        width - 40,
        height - 40
    )

    c.setStrokeColor(colors.HexColor("#0A2342"))
    c.setLineWidth(2)

    c.rect(
        35,
        35,
        width - 70,
        height - 70
    )

    # ==========================================
    # HEADER
    # ==========================================

    c.setFillColor(colors.HexColor("#0A2342"))
    c.setFont("Times-Bold", 28)

    c.drawCentredString(
        width / 2,
        height - 80,
        "CV PORTAL"
    )

    c.setFillColor(colors.HexColor("#C9A227"))
    c.setFont("Times-Roman", 16)

    c.drawCentredString(
        width / 2,
        height - 110,
        "CERTIFICATE MANAGEMENT SYSTEM"
    )

    c.line(
        270,
        height - 120,
        width - 270,
        height - 120
    )

    # ==========================================
    # TITLE
    # ==========================================

    c.setFillColor(colors.HexColor("#0A2342"))
    c.setFont("Times-Bold", 34)

    c.drawCentredString(
        width / 2,
        height - 180,
        "CERTIFICATE OF COMPLETION"
    )

    # ==========================================
    # PRESENTED TO
    # ==========================================

    c.setFillColor(colors.black)
    c.setFont("Times-Roman", 18)

    c.drawCentredString(
        width / 2,
        height - 240,
        "This certificate is proudly presented to"
    )

    # ==========================================
    # NAME
    # ==========================================

    # Student Name
    c.setFillColor(colors.HexColor("#C99700"))
    c.setFont("Times-Bold", 32)

    c.drawCentredString(
    width / 2,
    height - 280,
    certificate.name
)

# Line under name
    c.setStrokeColor(colors.HexColor("#C99700"))
    c.line(
    250,
    height - 300,
    width - 250,
    height - 300
)

# Description
    c.setFillColor(colors.black)
    c.setFont("Times-Roman", 18)

    c.drawCentredString(
    width / 2,
    height - 360,
    "For successfully completing the internship program in"
)

# Domain Name (Moved lower)
    c.setFillColor(colors.HexColor("#1E5A88"))
    c.setFont("Times-Bold", 22)

    c.drawCentredString(
    width / 2,
    height - 400,
    certificate.domain.title()
)
    

    # ==========================================
    # DURATION
    # ==========================================

    c.setFillColor(colors.black)
    c.setFont("Times-Roman", 16)

    c.drawCentredString(
    width / 2,
    135,
    f"Duration : {certificate.start_date} to {certificate.end_date}"
)

    # ==========================================
    # CERTIFICATE ID
    # ==========================================

    c.setFont("Times-Bold", 14)

    c.drawCentredString(
    width / 2,
    95,
    f"Certificate ID : {certificate.certificate_id}"
)

    # ==========================================
    # LEFT SIGNATURE
    # ==========================================

    c.setStrokeColor(colors.HexColor("#0A2342"))
    c.setLineWidth(1.5)



    c.setFont("Times-Bold", 12)

    c.line(
    130,
    75,
    280,
    75
)
    c.drawCentredString(
    205,
    55,
    "AUTHORIZED SIGNATORY"
)

    # ==========================================
    # RIGHT SIGNATURE
    # ==========================================

    c.line(
    width - 180,
    75,
    width - 280,
    75
)

    c.drawCentredString(
    width - 205,
    55,
    "DIRECTOR"
)

    # ==========================================
    # QR CODE
    # ==========================================
    qr_data = (
        f"Certificate ID: {certificate.certificate_id}\n"
        f"Name: {certificate.name}\n"
        f"Domain: {certificate.domain}"
    )

    qr = qrcode.make(qr_data)

    qr_path = os.path.join(
        certificate_dir,
        f"{certificate.certificate_id}_qr.png"
    )

    qr.save(qr_path)

    c.drawImage(
    qr_path,
    width - 140,
    35,
    width=65,
    height=65
)

    # ==========================================
    # FOOTER
    # ==========================================

    c.setFillColor(colors.HexColor("#0A2342"))

    c.rect(
        0,
        0,
        width,
        30,
        fill=1
    )

    c.setFillColor(colors.white)
    c.setFont("Helvetica", 10)

    c.drawCentredString(
        width / 2,
        10,
        "CV Portal • Certificate Management System • 2026"
    )

    c.save()

    return pdf_path