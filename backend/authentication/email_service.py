from django.core.mail import EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_certificate_email(student_name, student_email, pdf_path):
    try:
        subject = "Internship Completion Certificate"

        body = f"""
Dear {student_name},

Greetings from CONZURA Soft Solutions.

We are pleased to inform you that you have successfully completed your internship program with us.

Please find your Internship Completion Certificate attached to this email for your reference and future use.

We appreciate your dedication and participation during the internship period and wish you continued success in your academic and professional endeavors.

Note:
This is an automatically generated email. Please do not reply to this message. If you have any queries, kindly contact our HR team.

Best Regards,

HR Team
CONZURA Soft Solutions
🌐 www.conzuragroups.com
📧 hr.india@conzuragroups.in
📞 +91 91646 26625

This is a system-generated email. No signature is required.
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