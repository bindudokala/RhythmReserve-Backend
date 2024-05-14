from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import get_user_model, authenticate, login as auth_login
from django.conf import settings
import json
from venue_auth.models import VenueUser
import boto3
from django.core.files.base import ContentFile
import uuid


@csrf_exempt
def venue_signup(request):
    if request.method == 'POST':
        #get info
        email = request.POST.get('email')
        password = request.POST.get('password')
        venueName = request.POST.get('venueName')
        location = request.POST.get('location')
        
        #handle file upload
        image_file = request.FILES.get('image', None)
        if image_file:
            #generate unique file name
            file_name = f"{uuid.uuid4()}{image_file.name}"
            #s33 upload logic
            s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            s3_client.upload_fileobj(image_file, settings.AWS_STORAGE_BUCKET_NAME, file_name)
            image_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_name}"
        else:
            image_url = None

        if not email or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)

        if VenueUser.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already in use'}, status=400)

        venue_user = VenueUser.objects.create_venue_user(email=email, password=password, venue_name=venueName, location=location, venue_image=image_url)
        venue_user.save()

        auth_login(request, venue_user)

        return JsonResponse({'success': 'Venue user created successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
@csrf_exempt
def venue_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)

        try:
            #retrieve user by email
            user = VenueUser.objects.get(email=email)
            
            #check if correct password
            if user.check_password(password):
                #if password correct, login
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                return JsonResponse({'success': 'Logged in successfully'}, status=200)
            else:
                #password is incorrect
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except VenueUser.DoesNotExist:
            #email does not exist in the database
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def get_venue_data(request):
    if request.method == "GET":
        data = json.loads(request.body)
        print("Received data:", data)
        email = data.get('email')
        venue = VenueUser.objects.get(email=email)

        if venue:
            return JsonResponse({'venue_name': venue.venue_name,
                                 'location': venue.location,
                                 'email': venue.email,
                                 'venue_image': venue.venue_image
                                }, status=200)
        else:
            return JsonResponse({'error', 'Invalid user session'}, status=405)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
