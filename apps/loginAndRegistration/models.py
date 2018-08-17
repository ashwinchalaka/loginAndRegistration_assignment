from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        inRegistration = False
        if 'first_name' in postData:
            inRegistration = True
        if inRegistration:
            if len(postData['first_name'].strip()) < 2:
                errors["first_name"] = "First name should be at least 2 characters"
            if len(postData['last_name'].strip()) < 2:
                errors["last_name"] = "Last name should be at least 2 characters"
            if not EMAIL_REGEX.match(postData['email'].strip().lower()):
                errors['email'] = "Invalid email"
            if len(postData['password'].strip()) < 8:
                errors["password"] = "Password should be at least 8 characters"
            if postData['conf_password'].strip() != postData['password'].strip():
                errors['conf_password'] = "Passwords do not match"
        else:
            if not EMAIL_REGEX.match(postData['email'].strip().lower()) or len(postData['password'].strip()) < 8:
                errors["password"] = "Invalid email or password"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    # Overidding the objects attribute value
    objects = UserManager()