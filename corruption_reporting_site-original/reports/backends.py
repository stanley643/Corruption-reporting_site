# backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import hashlib

class PhoneAuthenticationBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            phone_hash = hashlib.sha256(phone_number.encode()).hexdigest()
            user = UserModel.objects.get(phone_number=phone_hash)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
