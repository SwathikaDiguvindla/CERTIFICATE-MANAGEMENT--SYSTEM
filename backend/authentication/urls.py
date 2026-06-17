from django.urls import path
from . import views

urlpatterns = [
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password_view, name='reset_password'),

    path(
        'generate-certificate/',
        views.generate_certificate_view,
        name='generate_certificate'
    ),
    path(
    'download-certificate/<str:certificate_id>/',
    views.download_certificate,
    name='download_certificate'
),
]