from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def email_exist(value):
    if User.objects.filter(email=value):
        raise ValidationError(f'{value} already exists.')
    return True
