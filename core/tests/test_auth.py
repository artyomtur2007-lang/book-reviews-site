from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class AuthTests(TestCase):

    def test_user_registration(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'testuser')

    def test_user_login(self):
        User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        login = self.client.login(
            username='testuser',
            password='testpass123'
        )
        self.assertTrue(login)