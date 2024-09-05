from django import forms
from django.contrib.auth import authenticate
from .models import SaveImage

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        if not user:
            raise forms.ValidationError("Invalid login credentials")
        return self.cleaned_data

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = SaveImage
        fields = ['image']