from django.shortcuts import render, redirect
from .models import Certificate
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .utils import generate_certificate_pdf
from django.conf import settings
import re
from django.http import FileResponse

# ── helpers ──────────────────────────────────────────────
def is_strong_password(password):
    """At least 1 letter, 1 digit, 1 special character, min 8 chars."""
    if len(password) < 8 or len(password) > 15:
        return False, "Password must be between 8 and 15 characters."
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter."
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number."
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        return False, "Password must contain at least one special character."
    return True, ""

# ── login ─────────────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            # Check if username exists to give specific message
            if User.objects.filter(username=username).exists():
                error = "Incorrect password. Please try again."
            else:
                error = "Username not found. Please check and try again."

    return render(request, 'authentication/login.html', {'error': error})

# ── logout ────────────────────────────────────────────────
def logout_view(request):
    logout(request)
    return redirect('/login/')

# ── dashboard ─────────────────────────────────────────────
@login_required(login_url='/login/')
def dashboard_view(request):

    certificates = Certificate.objects.all().order_by('-id')

    return render(
        request,
        'authentication/dashboard.html',
        {
            'certificates': certificates,
            'total_certificates': certificates.count()
        }
    )
# ── forgot password ───────────────────────────────────────
def forgot_password_view(request):
    message = None
    error = None

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        users = User.objects.filter(email=email)

        if users.exists():
            user = users.first()
            # Generate reset token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"http://127.0.0.1:8000/reset-password/{uid}/{token}/"

            # Send email
            send_mail(
                subject="CV Portal — Password Reset",
                message=f"Hi {user.username},\n\nClick the link below to reset your password:\n\n{reset_link}\n\nThis link expires in 24 hours.\n\nIf you didn't request this, ignore this email.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            message = "Password reset link sent! Check your email."
        else:
            error = "No account found with that email address."

    return render(request, 'authentication/forgot_password.html', {'message': message, 'error': error})

# ── reset password ────────────────────────────────────────
def reset_password_view(request, uidb64, token):
    error = None
    success = None

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        error = "This reset link is invalid or has expired."
        return render(request, 'authentication/reset_password.html', {'error': error})

    if request.method == 'POST':
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if password1 != password2:
            error = "Passwords do not match."
        else:
            valid, msg = is_strong_password(password1)
            if not valid:
                error = msg
            else:
                user.set_password(password1)
                user.save()
                success = "Password reset successful! You can now log in."

    return render(request, 'authentication/reset_password.html', {
        'error': error,
        'success': success,
        'uidb64': uidb64,
        'token': token
    })
# ── generate certificate ────────────────────────────────
@login_required(login_url='/login/')
def generate_certificate_view(request):

    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        domain = request.POST.get("domain")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        # Generate next certificate ID

        last_number = 0

        certificates = Certificate.objects.filter(
            certificate_id__startswith="CERT2026"
        )

        for cert in certificates:
            try:
                number = int(cert.certificate_id[-4:])
                if number > last_number:
                    last_number = number
            except ValueError:
                pass

        new_number = last_number + 1

        certificate_id = f"CERT2026{new_number:04d}"

        # Save certificate

        certificate = Certificate.objects.create(
            certificate_id=certificate_id,
            name=name,
            phone=phone,
            email=email,
            domain=domain,
            start_date=start_date,
            end_date=end_date
        )

        # Generate PDF

        pdf_path = generate_certificate_pdf(certificate)

        certificate.pdf_file = pdf_path.replace(
            str(settings.MEDIA_ROOT) + "\\",
            ""
        )

        certificate.save()

        messages.success(
            request,
            f"Certificate {certificate_id} generated successfully!"
        )

        return redirect('/dashboard/')

    return render(
        request,
        "authentication/generate_certificate.html"
    )



from django.http import FileResponse
from django.shortcuts import get_object_or_404


@login_required(login_url='/login/')
def download_certificate(request, certificate_id):

    certificate = get_object_or_404(
        Certificate,
        certificate_id=certificate_id
    )

    if certificate.pdf_file:
        return FileResponse(
            certificate.pdf_file.open('rb'),
            as_attachment=True,
            filename=f"{certificate.certificate_id}.pdf"
        )

    return redirect('/dashboard/')