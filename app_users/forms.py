from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms

User = get_user_model()

class CustomFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "form-control",
                    'style': 'border: 2px solid white; border-radius: 0.5rem;',  # Adjust as needed
                }
            )

class UserRegisterForm(CustomFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password1", "password2"]

class UpdateAccountForm(CustomFormMixin ,forms.ModelForm):
    new_password = forms.CharField(
        label="New Password", 
        required=False, 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        label="Confirm Password", 
        required=False, 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        exclude = [
            "username", "password", "last_login", "user_permissions", "is_superuser", 
            "groups", "is_staff", "is_active", "date_joined", "bio", "occupation"
        ]

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
