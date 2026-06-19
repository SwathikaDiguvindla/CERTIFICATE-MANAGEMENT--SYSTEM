from django.contrib import admin
from .models import Student, Certificate, EmailLog

admin.site.register(Student)
admin.site.register(Certificate)
admin.site.register(EmailLog)