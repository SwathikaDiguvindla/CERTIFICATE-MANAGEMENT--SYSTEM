import os
import qrcode
from datetime import datetime
from django.conf import settings

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape  # Added landscape
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.urls import path
from . import views

def generate_certificate_pdf(certificate):

    # ==========================================
    # Create certificates folder
    # ==========================================
    certificate_dir = os.path.join(settings.MEDIA_ROOT, "certificates")
    os.makedirs(certificate_dir, exist_ok=True)

    pdf_path = os.path.join(certificate_dir, f"{certificate.certificate_id}.pdf")

    # ==========================================
    # Safe Date Parsing (Fixes the AttributeError)
    # ==========================================
    # Convert string dates from the form into datetime objects safely
    if isinstance(certificate.start_date, str):
        start_date_obj = datetime.strptime(certificate.start_date, '%Y-%m-%d')
    else:
        start_date_obj = certificate.start_date

    if isinstance(certificate.end_date, str):
        end_date_obj = datetime.strptime(certificate.end_date, '%Y-%m-%d')
    else:
        end_date_obj = certificate.end_date

    # ==========================================
    # Create Landscape PDF (Matches professional certificate layouts)
    # ==========================================
    c = canvas.Canvas(pdf_path, pagesize=landscape(A4))
    width, height = landscape(A4) # width is now ~841, height is ~595

    # ==========================================
    # Background Image
    # ==========================================
    bg_path = os.path.join(
        settings.BASE_DIR, "authentication", "static", "images", "certificate_bg.png"
    )
    c.drawImage(ImageReader(bg_path), 0, 0, width=width, height=height)

    # ==========================================
    # Today's Date
    # ==========================================
    today = datetime.today().strftime("%B %d, %Y")
    c.setFillColor(colors.black)
    c.setFont("Times-BoldItalic", 12)
    
    # Repositioned for landscape layout
    c.drawRightString(width - 80, height - 100, today)

    # ==========================================
    # Paragraph Style
    # ==========================================
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "Times-Roman"
    style.fontSize = 16
    style.leading = 28
    style.alignment = 1  # 1 changes text alignment to CENTERED

    # ==========================================
    # Certificate Content
    # ==========================================
    content = f"""
    This is to certify that <b>{certificate.name}</b> has successfully completed
    the internship at <u>Conzura Soft Solutions</u> from
    <b>{start_date_obj.strftime('%d %B %Y')}</b> to
    <b>{end_date_obj.strftime('%d %B %Y')}</b>.
    <br/><br/>
    During the internship period, the intern worked with dedication,
    sincerity and professionalism. The intern actively participated
    in assigned tasks and demonstrated good learning ability,
    teamwork and technical understanding throughout the internship
    program in <b>{certificate.domain}</b>.
    <br/><br/>
    We appreciate the intern's efforts and contribution to the organization
    during the internship tenure. We wish them success in all future
    academic and professional endeavors.
    """

    paragraph = Paragraph(content, style)
    
    # Wrapped to fit nicely in a landscape container width
    paragraph.wrapOn(c, 650, 300)
    # X=96 centers the 650-wide block perfectly on the 841-wide canvas
    paragraph.drawOn(c, 96, 180) 

    # ==========================================
    # Certificate ID
    # ==========================================
    c.setFont("Helvetica-Bold", 11)
    c.drawString(80, 50, f"Certificate ID : {certificate.certificate_id}")

    # ==========================================
    # QR Code
    # ==========================================
    qr_data = f"""Certificate ID : {certificate.certificate_id}
Name : {certificate.name}
Email : {certificate.email}
Phone : {certificate.phone}
Domain : {certificate.domain}
Duration : {start_date_obj.strftime('%Y-%m-%d')} to {end_date_obj.strftime('%Y-%m-%d')}"""

    qr = qrcode.make(qr_data)
    qr_path = os.path.join(certificate_dir, f"{certificate.certificate_id}_qr.png")
    qr.save(qr_path)

    # Placed on the bottom right side of the landscape canvas
    c.drawImage(qr_path, width - 130, 35, width=70, height=70)

    # ==========================================
    # Save PDF
    # ==========================================
    c.save()
    return pdf_path
    