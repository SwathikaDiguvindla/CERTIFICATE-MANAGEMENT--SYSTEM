from django.db import models


class Certificate(models.Model):

    certificate_id = models.CharField(
        max_length=50,
        unique=True
    )

    name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField()

    domain = models.CharField(
        max_length=100
    )

    start_date = models.DateField()

    end_date = models.DateField()


    # PDF certificate file
    pdf_file = models.FileField(
        upload_to='certificates/',
        blank=True,
        null=True
    )


    # QR code image (for Member 3 integration)
    qr_code = models.ImageField(
        upload_to='qr_codes/',
        blank=True,
        null=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.name