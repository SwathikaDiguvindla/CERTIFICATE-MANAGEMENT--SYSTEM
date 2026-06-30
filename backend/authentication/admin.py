from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

@login_required
def add_member_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("add_member")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("add_member")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # assign default role
        student_group, _ = Group.objects.get_or_create(name="Student")
        user.groups.add(student_group)

        messages.success(request, "Member created successfully!")
        return redirect("dashboard")

    return render(request, "authentication/add_member.html")