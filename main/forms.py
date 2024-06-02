# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from main.models import ContactMessage, UserProfile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class ContactForm(forms.ModelForm):
    name = forms.CharField(label="Ім'я", max_length=100)
    email = forms.EmailField(label="Email")
    message = forms.CharField(label="Повідомлення", widget=forms.Textarea)

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['additional_field']