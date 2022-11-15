from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

User = get_user_model()


class UserTest(APITestCase):
    __username_admin = 'admin'
    __email_admin = 'admin@admin.com'
    __username = 'test{}'
    __email = 'test{}@test.com'
    __password = 'test1234qwesdwqe'
    __url_user = reverse('user')
    __url_user_detail = reverse('user-detail')

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username=cls.__username_admin,
                                        password=cls.__password,
                                        email=cls.__email_admin)
        user.is_staff = True
        user.save()

        for i in range(3):
            User.objects.create_user(username=cls.__username.format(i),
                                     password=cls.__password,
                                     email=cls.__email.format(i))

    def _authorization(self, username):
        url = reverse('jwt-create')
        user_data = {'username': username, 'password': self.__password}
        response = self.client.post(url, data=user_data)
        access_token = response.data.get('access')

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + access_token)
        return client

    def test_endpoints_users_if_logout(self):
        response = self.client.get(self.__url_user)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_endpoints_me_if_logout(self):
        response = self.client.get(self.__url_user_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_endpoints_users_if_login_admin(self):
        client = self._authorization(self.__username_admin)
        response = client.get(self.__url_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), User.objects.count())

    def test_get_endpoints_users_if_login_user(self):
        username = self.__username.format(0)
        client = self._authorization(username)
        response = client.get(self.__url_user)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].get('username'), username)

    def test_get_endpoints_me_show_balance(self):
        username = self.__username.format(1)
        client = self._authorization(username)
        response = client.get(self.__url_user_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data.get('username'), username)
        self.assertTrue(data.get('balance'))

    def test_post_endpoints_users(self):
        number = 5
        username = self.__username.format(number)
        first_name = 'Ivan'
        last_name = 'Petrov'
        data = {
            'username': username,
            'password': self.__password,
            're_password': self.__password,
            'email': self.__email.format(number),
            'first_name':  first_name,
            'last_name': last_name
        }

        response = self.client.post(self.__url_user, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.filter(username=username)[0]
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
