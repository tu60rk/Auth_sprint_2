import http

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
        response = requests.post(
            url,
            json=payload,
        )
        if response.status_code != http.HTTPStatus.ACCEPTED:
            return None

        data = response.json()
        response = requests.get(
            url='http://auth_service:8000/api/v1/users/me',
            headers={'Authorization': f'Bearer {data.get("access_token")}'}
        )
        data = response.json()
        try:
            user, created = User.objects.get_or_create(id=data['id'],)
            user.email = data.get('email')
            user.first_name = data.get('first_name', 'test')
            user.last_name = data.get('last_name', 'test')
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
