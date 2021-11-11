from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import ConservationCategory, ConservationContent, BirdingCategory, BirdingContent

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

class AddConservationCategory(forms.ModelForm):
    class Meta:
        model = ConservationCategory
        fields = ["conservation_category", "category_summary", "category_image"]
        labels = {"conservation_category": "Category Name", "category_summary": "Category Summary", "category_image": ""}
        widgets = {"category_summary": forms.Textarea(attrs={"class": "materialize-textarea"}), "category_image": forms.FileInput(attrs={"style": "display: none;", "accept": "image/*"})}

class AddConservationContent(forms.ModelForm):
    class Meta:
        model = ConservationContent
        fields = ["conservation_content", "content_text", "content_file", "content_category"]
        labels = {"conservation_content": "Content Title", "content_text": "Content Text", "content_file": "", "content_category": "Content Category (FK)"}
        widgets = {"content_text": forms.Textarea(attrs={"class": "materialize-textarea"}), "content_file": forms.FileInput(attrs={"style": "display: none;"}), "content_category": forms.HiddenInput()}

class EditConservationCategory(forms.Form):
    data_id = forms.CharField(widget=forms.HiddenInput())
    data_type = forms.CharField(widget=forms.HiddenInput())
    data_next = forms.CharField(widget=forms.HiddenInput())
    conservation_category = forms.CharField(label="Category Name", max_length=100)
    category_summary = forms.CharField(widget=forms.Textarea(attrs={"class": "materialize-textarea"}), label="Category Summary", max_length=500)

class EditConservationContent(forms.Form):
    data_id = forms.CharField(widget=forms.HiddenInput())
    data_type = forms.CharField(widget=forms.HiddenInput())
    data_next = forms.CharField(widget=forms.HiddenInput())
    conservation_content = forms.CharField(label="Category Name", max_length=100)
    content_text = forms.CharField(widget=forms.Textarea(attrs={"class": "materialize-textarea"}), label="Content Text")

class AddBirdingCategory(forms.ModelForm):
    class Meta:
        model = BirdingCategory
        fields = ["birding_category", "category_summary", "category_image"]
        labels = {"birding_category": "Category Name", "category_summary": "Category Summary", "category_image": ""}
        widgets = {"category_summary": forms.Textarea(attrs={"class": "materialize-textarea"}), "category_image": forms.FileInput(attrs={"style": "display: none;", "accept": "image/*"})}

class AddBirdingContent(forms.ModelForm):
    class Meta:
        model = BirdingContent
        fields = ["birding_content", "content_text", "content_file", "content_category"]
        labels = {"birding_content": "Content Title", "content_text": "Content Text", "content_file": "", "content_category": "Content Category (FK)"}
        widgets = {"content_text": forms.Textarea(attrs={"class": "materialize-textarea"}), "content_file": forms.FileInput(attrs={"style": "display: none;"}), "content_category": forms.HiddenInput()}

class EditBirdingCategory(forms.Form):
    data_id = forms.CharField(widget=forms.HiddenInput())
    data_type = forms.CharField(widget=forms.HiddenInput())
    data_next = forms.CharField(widget=forms.HiddenInput())
    birding_category = forms.CharField(label="Category Name", max_length=100)
    category_summary = forms.CharField(widget=forms.Textarea(attrs={"class": "materialize-textarea"}), label="Category Summary", max_length=500)

class EditBirdingContent(forms.Form):
    data_id = forms.CharField(widget=forms.HiddenInput())
    data_type = forms.CharField(widget=forms.HiddenInput())
    data_next = forms.CharField(widget=forms.HiddenInput())
    birding_content = forms.CharField(label="Category Name", max_length=100)
    content_text = forms.CharField(widget=forms.Textarea(attrs={"class": "materialize-textarea"}), label="Content Text")
