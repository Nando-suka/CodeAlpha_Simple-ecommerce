from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=80, required=True, label="Name")

    class Meta:
        model = User
        fields = ["first_name", "username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        if commit:
            user.save()
        return user


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=120, label="Full name")
    email = forms.EmailField()
    shipping_address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), label="Shipping address")
    city = forms.CharField(max_length=80)
    postal_code = forms.CharField(max_length=20, label="Postal code")
