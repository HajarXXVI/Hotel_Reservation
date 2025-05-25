from django import forms
from allauth.account.forms import SignupForm
from django.utils.translation import gettext_lazy as _

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30,
        label=_('First Name'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('First Name'),
                'class': 'form-control'
            }
        )
    )
    last_name = forms.CharField(
        max_length=30,
        label=_('Last Name'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Last Name'),
                'class': 'form-control'
            }
        )
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': _('E-mail'),
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make sure these fields are included in the form
        self.fields['first_name'] = self.fields['first_name']
        self.fields['last_name'] = self.fields['last_name']
        self.fields['email'] = self.fields['email']
        # Add Bootstrap classes to password fields
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user 