from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    address = forms.CharField(
        max_length=255,
        required=False,
        help_text="Enter your street address"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit)
        profile = user.profile
        profile.address = self.cleaned_data['address']
        if commit:
            profile.save()
        return user

