from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
import json

# Create your test cases

User = get_user_model()

class UserAuthViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_index_view(self):
        # Test the index view
        url = reverse('user_auth:index')  # Assuming you have a URL pattern with the name 'index'
        response = self.client.get(url)

        # Check that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the content of the response matches the expected text
        self.assertEqual(response.content.decode('utf-8'), "Hello, world. You're at the auth index.")

    def test_signup_view(self):
        # Test the signup view
        url = reverse('user_auth:signup')  # Assuming you have a URL pattern with the name 'signup'
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'phoneNumber': '1234567890',
            'spotifyUsername': 'test_spotify_user',
            'firstName': 'Test',
            'lastName': 'User',
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json')

        # Check that the response has a status code of 201 (Created) for a successful signup
        self.assertEqual(response.status_code, 201)

        # Add more assertions as needed for successful and unsuccessful signup scenarios

    def test_login_view(self):
        # Test the login view
        url = reverse('user_auth:login')  # Assuming you have a URL pattern with the name 'login'
        data = {
            'usernameOrEmail': 'testuser',
            'password': 'testpassword',
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json')

        # Check that the response has a status code of 200 (OK) for a successful login
        self.assertEqual(response.status_code, 200)

        # Add more assertions as needed for successful and unsuccessful login scenarios

        # Example of an assertion for an unsuccessful login
        invalid_data = {
            'usernameOrEmail': 'nonexistentuser',
            'password': 'invalidpassword',
        }
        invalid_response = self.client.post(url, json.dumps(invalid_data), content_type='application/json')
        self.assertEqual(invalid_response.status_code, 400)

    def run_all_tests(self):
        # Run all the test methods
        self.test_index_view()
        self.test_signup_view()
        self.test_login_view()

        # Print a statement indicating that all tests have passed
        print("All tests passed!")

# If this script is run as the main program (not imported as a module), run the tests
if __name__ == "__main__":
    test_case = UserAuthViewsTestCase()
    test_case.run_all_tests()