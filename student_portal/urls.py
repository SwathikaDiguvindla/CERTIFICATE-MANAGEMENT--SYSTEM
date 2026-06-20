from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_certificate, name='search'),
    path('download/<int:id>/', views.download_certificate, name='download'),
]