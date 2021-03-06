from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from rest_framework.authtoken.models import Token

User = get_user_model()


class TestUserAPI:

    @property
    def _get_stub_context(self):
        return {
            'user_id': 'example',
            'password': 'asd',
            'email': 'ex@ex.com',
        }

    def _create_stub_user(self, client):
        context = self._get_stub_context
        response = client.post(resolve_url('api:users:user_create'), context)
        return response

    def _get_response_with_token(self, client):
        context = self._get_stub_context
        context.pop('email')

        response = client.post(resolve_url('api:users:user_login'), context)
        return response

    def test_create_member_api(self, client):
        response = self._create_stub_user(client)

        assert response.status_code == 201
        assert response.json()['token'] == Token.objects.get(user=User.objects.first()).key

    def test_error_occurs_when_duplication_the_id_or_email(self, client):
        context = self._get_stub_context
        self._create_stub_user(client)

        context['email'] = 'ex2@ex.com'
        response = client.post(resolve_url('api:users:user_create'), context)

        assert response.status_code == 400, 'id가 중복되어 생성되면 안된다.'
        assert response.data.get('user_id')

        context['email'] = 'ex@ex.com'
        context['user_id'] = 'differentID'
        response = client.post(resolve_url('api:users:user_create'), context)

        assert response.status_code == 400, 'email이 중복되어 생성되면 안된다.'
        assert response.data.get('email')

    def test_user_login_api(self, client):
        self._create_stub_user(client)
        response = self._get_response_with_token(client)

        assert response.status_code == 200, '성공적으로 로그인되어야한다.'
        assert response.json()['token'] == Token.objects.get(user=User.objects.first()).key

    def test_user_profile_api(self, client):
        self._create_stub_user(client)

        response = client.get(resolve_url('api:users:user_profile', pk=1))

        assert response.status_code == 200, '성공적으로 프로필을 가져온다.'
        assert response.json()['user_id']
        assert response.json()['email']
        assert not response.json().get('password')

    def test_user_profile_api_user_not_found(self, client):
        self._create_stub_user(client)

        response = client.get(resolve_url('api:users:user_profile', pk=10))

        assert response.status_code == 404
