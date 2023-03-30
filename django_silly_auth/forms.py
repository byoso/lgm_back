from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        max_length=64, widget=forms.PasswordInput,
        validators=[MinLengthValidator(4), MaxLengthValidator(64)]
    )
    password2 = forms.CharField(
        label="Confirm password",
        max_length=64, widget=forms.PasswordInput,
        validators=[MinLengthValidator(4), MaxLengthValidator(64)]
    )

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise ValidationError("Passwords don't match, do it again")
        return password2
