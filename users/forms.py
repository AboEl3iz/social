from django import forms
from django.contrib.auth.models import User
from .models import Profile, Settings

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['privacy', 'email_notifications', 'profile_visible']