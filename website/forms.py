from django import forms
from .models import UserRegistration,JobApplication,Address,User
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
import re


#REGISTRATION FORM
def validate_name(value):
    if not re.match("^[A-Za-z\s]+([ '-][A-Za-z\s]+)*$", value):
        raise ValidationError("Name should only contain letters and spaces.")
    if not value.replace(" ", "").isalpha():
        raise forms.ValidationError('Name should only contain letters and spaces.')
    if len(value) < 4:
        raise forms.ValidationError('Name should be at least 4 characters long.')
    return value
    
def validate_password(value):
    if len(value) < 8:
        raise forms.ValidationError('Password must be at least 8 characters long.')
    if not any(char.isdigit() for char in value):
        raise forms.ValidationError('Password must contain at least one digit.')
    if not any(char.isalpha() for char in value):
        raise forms.ValidationError('Password must contain at least one letter.')
    if not re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", value):
        raise ValidationError("Password should be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one digit, and one special character.")
    return value

def validate_email(value):
    if not re.match("^[a-zA-Z]+[a-zA-Z0-9]*@gmail\.com$", value):
        raise ValidationError("Email should be in the format of 'username@gmail.com' and start with letters.")

class UserRegistrationForm(forms.ModelForm):
    password_suggestion = forms.CharField(label='Password Suggestion', required=False, widget=forms.TextInput(attrs={'autocomplete': 'on'}))

    class Meta:
        model = UserRegistration
        fields = ('first_name', 'last_name', 'email', 'password', 'confirm_password')

    def _validate_required_fields(self, cleaned_data):
        for field in ['first_name', 'last_name', 'email', 'password', 'confirm_password']:
            if not cleaned_data.get(field):
                self.add_error(field, f'{field.capitalize()} is required')

    def clean(self):
        cleaned_data = super().clean()
        self._validate_required_fields(cleaned_data)

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')

        if self.cleaned_data.get('password_suggestion'):
            cleaned_data['password'] = self.cleaned_data['password_suggestion']
            cleaned_data['confirm_password'] = self.cleaned_data['password_suggestion']

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['data-toggle'] = 'password'
        self.fields['confirm_password'].widget.attrs['data-toggle'] = 'password'
        self.fields['first_name'].validators = [validate_name]
        self.fields['last_name'].validators = [validate_name]
        self.fields['password'].validators = [validate_password]
        self.fields['confirm_password'].validators = [validate_password]
        self.fields['email'].validators = [validate_email]


# JOB APPLICATION FORM
class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ('first_name', 'last_name', 'email_address', 'phone_number', 'position_applied_for', 'resume_cv', 'cover_letter', 'current_level_of_experience', 'earliest_possible_start_date')

    def _validate_name_field(self, field_name, field_value):
        if not re.match(r'^[a-zA-Z\s]+$', field_value):
            raise forms.ValidationError(f'{field_name.capitalize()} should only contain letters and spaces')
        if len(field_value) < 4:
            raise forms.ValidationError(f'{field_name.capitalize()} should be at least 4 characters long')
        return field_value

    def _validate_email_address(self, email_address):
        if not re.match(r'^[a-zA-Z0-9_.+-]+@gmail\.com$', email_address):
            raise forms.ValidationError('Invalid email address format. Only Gmail addresses are allowed')
        return email_address

    def _validate_phone_number(self, phone_number):
        if len(phone_number) < 10:
            raise forms.ValidationError('Phone number must be at least 10 digits long.')
        return phone_number

    def _validate_earliest_possible_start_date(self, earliest_possible_start_date):
        if earliest_possible_start_date < timezone.now().date():
            raise forms.ValidationError('Earliest possible start date cannot be in the past')
        return earliest_possible_start_date

    def clean_first_name(self):
        return self._validate_name_field('first_name', self.cleaned_data.get('first_name'))

    def clean_last_name(self):
        return self._validate_name_field('last_name', self.cleaned_data.get('last_name'))

    def clean_email_address(self):
        return self._validate_email_address(self.cleaned_data.get('email_address'))

    def clean_phone_number(self):
        return self._validate_phone_number(self.cleaned_data.get('phone_number'))

    def clean_earliest_possible_start_date(self):
        return self._validate_earliest_possible_start_date(self.cleaned_data.get('earliest_possible_start_date'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['email_address'].label = 'Email Address'
        self.fields['phone_number'].label = 'Phone Number'
        self.fields['position_applied_for'].label = 'Position Applied For'
        self.fields['resume_cv'].label = 'Resume/CV (PDF only)'
        self.fields['cover_letter'].label = 'Cover Letter'
        self.fields['current_level_of_experience'].label = 'Current Level of Experience'
        self.fields['earliest_possible_start_date'].label = 'Earliest Possible Start Date'
        self.fields['phone_number'].widget.attrs['pattern'] = '[0-9]{10,}'
        self.fields['phone_number'].widget.attrs['title'] = 'Phone number must be at least 10 digits long.'


#LOGIN FORM
class LoginForm(forms.ModelForm):
    model = User
    fields = ('email','password')
    