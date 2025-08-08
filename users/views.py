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
from django.template.loader import render_to_string

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
            welcome_message = f"""
            Welcome to SocialHub, {user.username}!
            
            Thank you for joining our community. Here's what you can do:
            - Create and share posts with images
            - Follow other users
            - Like and comment on posts
            - Search for users and content
            - Customize your profile and privacy settings
            
            Get started by creating your first post!
            
            Best regards,
            The SocialHub Team
            """
            send_mail(
                'Welcome to SocialHub!',
                welcome_message,
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

# Email notification functions
def send_like_notification(post, liker):
    """Send email notification when someone likes your post"""
    if post.user != liker and post.user.settings.email_notifications:
        subject = f'{liker.username} liked your post'
        message = f"""
        Hi {post.user.username},
        
        {liker.username} just liked your post: "{post.text[:50]}{'...' if len(post.text) > 50 else ''}"
        
        View your post: http://127.0.0.1:8000/posts/post/{post.id}/
        
        Best regards,
        SocialHub Team
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [post.user.email],
            fail_silently=True,
        )

def send_comment_notification(post, commenter):
    """Send email notification when someone comments on your post"""
    if post.user != commenter and post.user.settings.email_notifications:
        subject = f'{commenter.username} commented on your post'
        message = f"""
        Hi {post.user.username},
        
        {commenter.username} just commented on your post: "{post.text[:50]}{'...' if len(post.text) > 50 else ''}"
        
        Comment: "{commenter.comment_set.last().text}"
        
        View your post: http://127.0.0.1:8000/posts/post/{post.id}/
        
        Best regards,
        SocialHub Team
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [post.user.email],
            fail_silently=True,
        )

def send_follow_notification(follower, following):
    """Send email notification when someone follows you"""
    if following.settings.email_notifications:
        subject = f'{follower.username} started following you'
        message = f"""
        Hi {following.username},
        
        {follower.username} just started following you on SocialHub!
        
        View their profile: http://127.0.0.1:8000/users/profile/{follower.username}/
        
        Best regards,
        SocialHub Team
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [following.email],
            fail_silently=True,
        )
