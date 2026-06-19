from django.urls import path
from .views import verify_certificate, home

urlpatterns = [
    path('', home, name='home'),

    path(
        'verify/<str:certificate_id>/',
        verify_certificate,
        name='verify_certificate'
    ),
]