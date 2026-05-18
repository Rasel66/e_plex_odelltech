from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'password1', 'password2']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email',max_length=150,widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid email or password.")
            except User.MultipleObjectsReturned:
                raise forms.ValidationError("Multiple accounts found with this email.")

            self.user = authenticate(
                self.request,
                username=user_obj.username,
                password=password
            )
            if self.user is None:
                raise forms.ValidationError("Invalid email or password.")

        return self.cleaned_data

    def get_user(self):
        return self.user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'image']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This email is already in use.")
        return email