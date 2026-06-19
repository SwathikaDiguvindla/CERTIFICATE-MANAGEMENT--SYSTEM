from django.core.mail import EmailMessage
from django.conf import settings
import logging
logger = logging.getLogger(__name__)


def send_certificate_email(student_name, student_email, pdf_path):
    try:
        subject = "Certificate Generated Successfully"

        body = f"""
Dear {student_name},

Congratulations!

Your certificate has been generated successfully.

Please find your certificate attached.

Regards,
Certificate Management Team
"""

        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.EMAIL_HOST_USER,
            to=[student_email],
        )

        email.attach_file(pdf_path)
        email.send()

        return True

    except Exception as e:
        logger.error(f"Email Error: {e}")
        return False