from typing import Any
from django import forms
from django.contrib.auth import authenticate
from .models import Employee
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'address', 'phone_number', 'salary', 'designation', 'description']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input mt-1 block w-full h-12 pl-4 pr-4 rounded-lg border border-gray-300',  
                'placeholder': 'Enter full name',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-input mt-1 block w-full h-12 pl-4 pr-4 rounded-lg border border-gray-300',  
                'placeholder': 'Enter address',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-input mt-1 block w-full h-12 pl-4 pr-4 rounded-lg border border-gray-300',  
                'placeholder': 'Enter phone number',
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-input mt-1 block w-full h-12 pl-4 pr-4 rounded-lg border border-gray-300',
                'placeholder': '$ Enter salary',
            }),
            'designation': forms.Select(attrs={
                'class': 'border-gray-300 rounded-md p-2 w-full',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-input mt-1 block w-full h-12 pl-4 pr-4 rounded-lg border border-gray-300',
                'placeholder': 'Enter a brief profile summary',
                'rows': 1,
            }),
        }

    def __init__(self, *args, **kwargs):
        is_update = kwargs.pop('is_update', False)
        super(EmployeeForm, self).__init__(*args, **kwargs)

        if is_update:
            self.fields['salary'].widget.attrs['readonly'] = True
            self.fields['designation'].disabled = True

    def clean_designation(self):
        return self.initial['designation']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input mt-2 block w-full bg-white border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-base py-2 px-3',
                'placeholder': 'Enter your username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input mt-2 block w-full bg-white border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-base py-2 px-3',
                'placeholder': 'Enter your email'
            }),
        
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input mt-2 block w-full bg-white border border-gray-300 rounded-lg py-2 px-3',
        'placeholder': 'Enter your username',
        'autofocus': True
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input mt-2 block w-full bg-white border border-gray-300 rounded-lg py-2 px-3',
        'placeholder': 'Enter your password',
    }))




class CustomUserChangeForm(UserChangeForm):
    old_password = forms.CharField(
        label='Old Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Enter old password'}),
        required=False
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Enter new password'}),
        required=False
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm new password'}),
        required=False
    )


    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if old_password or new_password1 or new_password2:
            if not old_password:
                self.add_error('old_password', 'This field is required.')
            else:
                user = authenticate(username=self.instance.username, password=old_password)
                if not user:
                    self.add_error('old_password', 'Incorrect password.')

            if new_password1 and new_password2:
                if new_password1 != new_password2:
                    self.add_error('new_password2', 'Passwords do not match.')
            
            else:
                self.add_error('new_password1', 'This field is required.')

        return cleaned_data
                

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password1 = self.cleaned_data.get('new_password1')

        if new_password1:
            user.set_password(new_password1)
        if commit:
            user.save()
        return user
