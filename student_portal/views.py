from django.shortcuts import render
from django.http import FileResponse
from .models import Certificate

def home(request):
    return render(request, 'student.html')

def search_certificate(request):
    keyword = request.GET.get('keyword')

    certificate = Certificate.objects.filter(
        name=keyword
    ).first()

    if not certificate:
        certificate = Certificate.objects.filter(
            email=keyword
        ).first()

    if not certificate:
        certificate = Certificate.objects.filter(
            phone=keyword
        ).first()

    return render(
        request,
        'student.html',
        {'certificate': certificate}
    )

def download_certificate(request, id):
    certificate = Certificate.objects.get(id=id)

    return FileResponse(
        certificate.pdf_file.open(),
        as_attachment=True
    )