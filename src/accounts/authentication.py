from django.contrib.auth.backends import BaseBackend
from .models import *


class PhoneAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(phone=username)
            if user.check_password(password):
                return user

            return None
        except User.DoesNotExist:
            raise ValueError('+=')

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
