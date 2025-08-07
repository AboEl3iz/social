from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Settings
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm, ProfileForm, SettingsForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse

# Create your views here.

# Registration view

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user)
            Settings.objects.create(user=user)
            # Send welcome email
            send_mail(
                'Welcome to SocialHub!',
                'Thank you for registering at SocialHub.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# Login view

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home_feed')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# Logout view

def logout_view(request):
    logout(request)
    return redirect('login')

# Profile view
@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    posts = user.post_set.all()
    is_owner = request.user == user
    if is_owner:
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated!')
                return redirect('profile', username=user.username)
        else:
            form = ProfileForm(instance=profile)
    else:
        form = None
    return render(request, 'users/profile.html', {'profile': profile, 'posts': posts, 'is_owner': is_owner, 'form': form})

# Settings view
@login_required
def settings_view(request):
    settings_obj = Settings.objects.get(user=request.user)
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated!')
            return redirect('settings')
    else:
        form = SettingsForm(instance=settings_obj)
    return render(request, 'users/settings.html', {'form': form})

# Password reset view

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='users/password_reset_email.html',
                subject_template_name='users/password_reset_subject.txt',
            )
            messages.success(request, 'Password reset email sent!')
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'users/password_reset.html', {'form': form})
