import http
import uuid

import requests
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        url = 'http://auth_service:8000/api/v1/auth/login'
        payload = {
            'email': username,
            'password': password,
            'set_cookie': False
        }
        headers = {'X-Request-Id': str(uuid.uuid4())}
        response = requests.post(
            url,
            headers=headers,
            json=payload,
        )
        if response.status_code != http.HTTPStatus.ACCEPTED:
            return None

        data = response.json()
        try:
            user, created = User.objects.get_or_create(id=data.get('user_id'),)
            user.email = data.get('email')
            user.first_name = data.get('first_name')
            user.last_name = data.get('last_name')
            user.verified = True
            user.is_active = True
            user.save()
        except Exception:
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
