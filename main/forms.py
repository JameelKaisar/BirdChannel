from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from tinymce.widgets import TinyMCE

class MyRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(MyRegistrationForm, self).__init__(*args, **kwargs)
    username = forms.CharField(widget=forms.TextInput(attrs={"autocapitalize": "none", "autocomplete": "username", "maxlength": "150", "autofocus": "autofocus"}), label="Username")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}), label="Confirm Password")

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "autofocus": "autofocus"}), label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}), label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}), label="Confirm New Password")

class MyLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)
    username = forms.CharField(widget=forms.TextInput(attrs={"autocapitalize": "none", "autocomplete": "username", "maxlength": "150", "autofocus": "autofocus"}), label="Username")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}), label="Password")
