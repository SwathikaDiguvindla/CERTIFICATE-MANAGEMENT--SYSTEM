from django.db import models

class Certificate(models.Model):
    certificate_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    domain_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    pdf_file = models.FileField(upload_to='certificates/')

    def __str__(self):
        return self.name
