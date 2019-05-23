from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

CREATE_USER_URL = reverse('user:signup')
LOGIN_URL = reverse('user:login')
USER_URL = reverse('user:user')
HOME_URL = reverse('user:home')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class UserTestCase(TestCase):
    """Tests user model"""

    def setUp(self):
        self.client = Client()
        self.data = {
            'username': 'marian',
            'email': 'test@gmailcom',
            'password': 'marian1234',
        }

    def test_user_is_created(self):
        """Test user is created successfully"""
        get_user_model().objects.create_user(**self.data)
        user = get_user_model().objects.get(username=self.data['username'])

        self.assertIsNotNone(user)

    def test_user_is_created_with_unique_username(self):
        """Test user is created with unique username"""
        get_user_model().objects.create_user(**self.data)
        try:
            user = get_user_model().objects.create_user(**self.data)
        except Exception:
            user = None

        self.assertIsNone(user)

    def test_user_is_created_with_unique_email(self):
        """Test user is created with unique email"""
        get_user_model().objects.create_user(**self.data)
        data = {
            'username': 'damian',
            'email': 'test@gmailcom',
            'password': 'marian1234',
        }
        try:
            user = get_user_model().objects.create_user(**self.data)
        except Exception:
            user = None

        self.assertIsNone(user)


class UserApiTestCase(TestCase):
    """Test user web api"""
    def setUp(self):
        self.client = Client()
        self.data = {
            'username': 'marian',
            'email': 'test@gmailcom',
            'password': 'marian1234',
        }

    def test_signup_page(self):
        """Test signup page"""
        response = self.client.get(CREATE_USER_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')

    def test_login_page(self):
        """Test login page"""
        response = self.client.get(LOGIN_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')

    def test_logged_user_redirects(self):
        """Test logged user is redirected when success login"""
        user = get_user_model().objects.create_user(**self.data)
        response = self.client.post(LOGIN_URL,
                                    self.data,
                                    )

        self.assertRedirects(response, HOME_URL)

    def test_user_page(self):
        """Test user page"""
        user = get_user_model().objects.create_user(**self.data)
        self.client.post(LOGIN_URL, self.data)
        response = self.client.get(USER_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user.html')















