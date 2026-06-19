from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render

from .models import Certificate
from .serializers import CertificateSerializer


@api_view(['GET'])
def verify_certificate(request, certificate_id):
    try:
        certificate = Certificate.objects.get(
            certificate_id=certificate_id
        )

        serializer = CertificateSerializer(certificate)

        return Response({
            "status": "valid",
            "data": serializer.data
        })

    except Certificate.DoesNotExist:
        return Response({
            "status": "invalid"
        })


def home(request):
    return render(request, 'verify.html')