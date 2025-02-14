from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import main_user


class SignUpForm(UserCreationForm):
    class Meta:
        model = main_user
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    model = main_user
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# forms.py
from django import forms
from .models import Profile

class GraphSelectionForm(forms.Form):
    desired_profession = forms.ModelChoiceField(queryset=Profile.objects.values_list('desired_profession', flat=True).distinct(), empty_label="Select a profession")
