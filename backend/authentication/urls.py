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

    path(
        'download/<str:certificate_id>/',
        views.download_certificate,
        name='download_certificate'
    ),

    path(
        'bulk-upload/',
        views.bulk_upload_view,
        name='bulk_upload'
    ),

    path(
        'verify-certificate/',
        views.verify_certificate,
        name='verify_certificate'
    ),

    path('create-admin/', views.create_admin_view, name='create_admin'),
    path("add-member/", views.add_member_view, name="add_member"),
]