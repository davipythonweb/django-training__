from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label=_('Email'))
    
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': _('Nome de Usuário'),
        }
        help_texts = {
            'username': _('Máximo de 150 caracteres. Letras, números e @/./+/-/_ apenas.'),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith(('@gmail.com', '@outlook.com')):
            raise ValidationError(
                _('Por favor, use um email do Gmail ou Outlook.')
            )
        return email

class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=True, label=_('Email'))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': _('Primeiro nome'),
            'last_name': _('Último nome'),
            'email': _('Email'),
        }
