from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
import json

VenueUser = get_user_model()

class VenueAuthViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_venue_signup_view(self):
        # Test the venue_signup view
        url = reverse('venue_auth:venue_signup')  # Assuming you have a URL pattern with the name 'venue_signup'
        data = {
            'email': 'venue@example.com',
            'password': 'venuepassword',
            'first_name': 'Venue',
            'last_name': 'User',
            'location': 'Venue Location',
            'venueImage': 'base64encodedimage',  # Add a valid base64 encoded image if needed
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json')

        # Check that the response has a status code of 201 (Created) for a successful venue_signup
        self.assertEqual(response.status_code, 201)

        # Add more assertions as needed for successful and unsuccessful venue_signup scenarios

    def test_venue_login_view(self):
        # Test the venue_login view
        url = reverse('venue_auth:venue_login')  # Assuming you have a URL pattern with the name 'venue_login'
        data = {
            'email': 'venue@example.com',
            'password': 'venuepassword',
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json')

        # Check that the response has a status code of 200 (OK) for a successful venue_login
        self.assertEqual(response.status_code, 200)

        # Add more assertions as needed for successful and unsuccessful venue_login scenarios

        # Example of an assertion for an unsuccessful venue_login
        invalid_data = {
            'email': 'nonexistentvenue@example.com',
            'password': 'invalidpassword',
        }
        invalid_response = self.client.post(url, json.dumps(invalid_data), content_type='application/json')
        self.assertEqual(invalid_response.status_code, 400)
