from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import FileExtensionValidator,validate_email
from django.core.exceptions import ValidationError
from django.core import validators
import re

def validate_name(value):
    if not value.replace(" ", "").isalpha():
        raise ValidationError("Name should only contain letters and spaces.")
    if len(value) < 4:
        raise ValidationError("Name should be at least 4 characters long.")
    return value

def validate_password(value):
    if len(value) < 8:
        raise ValidationError('Password should be at least 8 characters long')
    if not any(char.isdigit() for char in value):
        raise ValidationError('Password should have at least one digit')
    if not any(char.isupper() for char in value):
        raise ValidationError('Password should have at least one uppercase letter')
    if not any(char.islower() for char in value):
        raise ValidationError('Password should have at least one lowercase letter')
    if not any(char in '!@#$%^&*()_+-=' for char in value):
        raise ValidationError('Password should have at least one special character')

class UserRegistration(models.Model):
    first_name = models.CharField(max_length=50, validators=[validate_name])
    last_name = models.CharField(max_length=50, validators=[validate_name])
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, validators=[validate_password])
    confirm_password = models.CharField(max_length=128, validators=[validate_password])

    def save(self, *args, **kwargs):
        if self.password != self.confirm_password:
            raise ValidationError('Password and confirm password do not match')
        super(UserRegistration, self).save(*args, **kwargs)
    
    def get_password(self, show=False):
        if show:
            return self.password
        else:
            return "**********"
        
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return self.password == make_password(raw_password)


class JobApplication(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=10)
    position_applied_for = models.CharField(max_length=255)
    resume_cv = models.FileField(upload_to='resumes/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    cover_letter = models.TextField()
    current_level_of_experience = models.CharField(max_length=20, choices=[
        ('Entry Level', 'Entry Level(0-3)'),
        ('Mid Level', 'Mid Level(3-7)'),
        ('Senior Level', 'Senior Level(7-13)'),
        ('Other', 'Other'),
    ])
    earliest_possible_start_date = models.DateField(null=True)
    consent_to_privacy_policy = models.BooleanField(null=True)


class Address(models.Model):
    street_address = models.CharField(max_length=255)
    street_address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    postal_zip_code = models.CharField(max_length=20)   


#LOGIN PAGE CREDENTIALS
class User(models.Model):
    email = models.EmailField(unique=True, null=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username