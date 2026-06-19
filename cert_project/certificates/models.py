from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    domain = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()


class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    certificate_id = models.CharField(max_length=50, unique=True)
    pdf_path = models.CharField(max_length=255)
    qr_path = models.CharField(max_length=255)
    date = models.DateField()


class EmailLog(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    sent_time = models.DateTimeField(auto_now_add=True)