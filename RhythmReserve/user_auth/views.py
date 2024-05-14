from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
import sendgrid
from sendgrid.helpers.mail import Mail
from django.conf import settings
from .models import PasswordResetRequest
import json
import random
import string
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context

User = get_user_model()


def index(request):
    return HttpResponse("Hello, world. You're at the auth index.")


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        print("Received data:", data)

        # get fields
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        phoneNumber = data.get('phoneNumber')
        spotifyUsername = data.get('spotifyUsername')
        print(spotifyUsername)
        firstName = data.get('firstName')
        lastName = data.get('lastName')

        # ensure all fields filled.
        if not (username or password or email or phoneNumber or firstName or lastName):
            print("Validation Error: Missing fields")
            return JsonResponse({'error': 'All fields are required'}, status=400)

        # database validation
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already in use'}, status=400)
        if User.objects.filter(phoneNumber=phoneNumber).exists():
            return JsonResponse({'error': 'Phone number already in use'}, status=400)
        if User.objects.filter(spotifyUsername=spotifyUsername).exists():
            return JsonResponse({'error': 'Spotify Username already in use'}, status=400)

        # valid user, lets save and login.
        user = User.objects.create_user(username=username, email=email, password=password,
                                        first_name=firstName, last_name=lastName, phoneNumber=phoneNumber, spotifyUsername=spotifyUsername)
        user.save()
        auth_login(request, user)

        return JsonResponse({'success': 'User created and logged in successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        # get fields
        data = json.loads(request.body)
        print("Received data:", data)
        email = data.get('email')
        password = data.get('password')
        user = None

        if email:
            user = authenticate(request, username=email, password=password)

            if user is not None:
                auth_login(request, user)
                return JsonResponse({'success': 'Logged in'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        else:
            return JsonResponse({'error': 'Username or Email is required'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def send_reset_email(email_to, reset_code):
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    from_email = 'ReserveRhythm@gmail.com'  # sendgrid email
    to_email = email_to
    subject = 'Your Password Reset Code'
    content = f'Hi there, \n\nYour password reset code is: {reset_code}\n\nPlease enter this code to proceed with resetting your password.'
    mail = Mail(from_email, to_email, subject, content)
    response = sg.send(mail)


@csrf_exempt
def password_reset_request(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        email = data.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            reset_code = PasswordResetRequest.generate_reset_code(user)
            # Call the send email function here
            send_reset_email(user.email, reset_code)
            return JsonResponse({'message': 'If your email address exists in our database, you will receive a password reset code.'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def verify_reset_code(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        email = data.get('email')
        submitted_code = data.get('resetCode')

        user = User.objects.filter(email=email).first()

        if user and PasswordResetRequest.verify_reset_code(user, submitted_code):
            return JsonResponse({'success': 'Reset code verified'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid reset code'}, status=400)


@csrf_exempt
def reset_password_post(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        email = data.get('email')
        new_password = data.get('password')

        user = User.objects.filter(email=email).first()
        if user:
            user.set_password(new_password)
            user.save()
            return JsonResponse({'success': 'Password has been reset successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def google_signin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        credential = data.get('credential')

        try:
            # Verify the Google ID token
            idinfo = id_token.verify_oauth2_token(
                credential, requests.Request())

            # Get the user's email from the ID token
            email = idinfo['email']
            print(email)

            # Check if the user exists in the database
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

            # Generate a JWT token for the user
            token = jwt.encode({'user_id': user.id},
                               settings.GOOGLE_AUTH_SECRET_KEY, algorithm='HS256')

            return JsonResponse({'token': token}, status=200)

        except ValueError:
            return JsonResponse({'error': 'Invalid Google ID token'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def google_signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        credential = data.get('credential')
        phoneNumber = data.get('phoneNumber')
        spotifyUsername = data.get('spotifyUsername')
        firstName = data.get('firstName')
        lastName = data.get('lastName')
        email = data.get('email')

        try:
            # Check if the user already exists in the database
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already in use'}, status=400)

            # Create a new user with the additional information
            user = User.objects.create_user(
                username=email,
                email=email,
                password=None,  # Set password to None for google users
                phoneNumber=phoneNumber,
                spotifyUsername=spotifyUsername,
                first_name=firstName,
                last_name=lastName
            )

            # Generate a JWT token for the user
            token = jwt.encode({'user_id': user.id},
                               settings.GOOGLE_AUTH_SECRET_KEY, algorithm='HS256')

            return JsonResponse({'token': token}, status=201)

        except ValueError:
            return JsonResponse({'error': 'Invalid Google ID token'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def google_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        credential = data.get('credential')
        try:
            # Verify the Google ID token
            idinfo = id_token.verify_oauth2_token(
                credential, requests.Request())

            # Get the user's email from the ID token
            email = idinfo['email']
            print(email)

            # Return the email as a JSON response
            return JsonResponse({'email': email})
        except ValueError:
            return JsonResponse({'error': 'Invalid Google ID token'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

#takes a user's email and returns the user's id 
@csrf_exempt
def get_user_id(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({'error': 'Email is required'}, status=400)

            User = get_user_model()
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        
            return JsonResponse({
                'id': user.id
            }, status=200)
    
        except Exception as e:
            logger.error(f'Unexpected error: {str(e)}')
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)


@csrf_exempt
def get_user_data(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')

        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        return JsonResponse({
            'username': user.username,
            'email': user.email,
            'phoneNumber': user.phoneNumber,  # Adjust field names as necessary
            'spotifyUsername': user.spotifyUsername,  # Adjust field names as necessary
            'firstName': user.first_name,
            'lastName': user.last_name,
            'cardNumber': user.card_number,
            'cardHolderName': user.cardholder_name,
            'cvv': user.cvv,
            'expMonth': user.exp_month,
            'expYear': user.exp_year,
            'zipCode': user.zip_code
        }, status=200)

    except json.JSONDecodeError as json_error:
        logger.error(f'JSON Decode Error: {str(json_error)}')
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)