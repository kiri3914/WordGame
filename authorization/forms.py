from django import forms
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


from .models import CustomerUser, Profile

class CustomerUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomerUser
        fields = ('username', 'email', 'phone_number')


class CustomerAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )
        

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'birth_date', 'country']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model = CustomerUser
        fields = ['username', 'email', 'phone_number']