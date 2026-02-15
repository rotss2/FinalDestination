from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "phone")
