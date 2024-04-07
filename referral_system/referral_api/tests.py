from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User

# Create your tests here.

class UserRegistrationTestCase(TestCase):
    def test_user_registration(self):
        client = APIClient()
        url = reverse('user-registration')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')

class UserDetailsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_user_details(self):
        client = APIClient()
        url = reverse('user-details')
        token = self.user.get_tokens_for_user()['access']
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')

class ReferralsEndpointTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='referrer', email='referrer@example.com', password='testpassword')
        self.referred_user = User.objects.create_user(username='referred', email='referred@example.com', password='testpassword')
        self.referred_user.referral_code = 'ABC123'
        self.referred_user.save()

    def test_referrals_endpoint(self):
        client = APIClient()
        url = reverse('referrals')
        token = self.user.get_tokens_for_user()['access']
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'referred')
        self.assertEqual(response.data[0]['email'], 'referred@example.com')
