import uuid

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Event
from django.utils import timezone
from django.conf import settings
import pytz
import json
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
import time
import boto3
from pytz import timezone
from django.utils.timezone import now


# Import VenueUser model
from venue_auth.models import VenueUser

def index(request):
    return HttpResponse("Event index")

@csrf_exempt
def event_detail(request, event_id):

    if request.method == 'GET':
        event = get_object_or_404(Event, id=event_id)

        readable_event_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(event.event_time)))

        event_details = {
            "id": event.id,
            "venue_user_email": event.venue_user_email,
            "event_name": event.event_name,
            "event_time": readable_event_time,
            "event_location": event.event_location,
            "event_image_url": event.event_image_url,
            "available_general_admission_tickets": event.available_general_admission_tickets,
            "general_admission_price": event.general_admission_price,
            "available_vip_tickets": event.available_vip_tickets,
            "vip_ticket_price": event.vip_ticket_price,
            "genre": event.genre,
            "description": event.description
        }

        # Convert event_time to string explicitly
        event_details['event_time'] = str(readable_event_time)

        return JsonResponse(event_details)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def get_est_timezone(request):
    # This function needs to accept 'request' to function correctly
    user_timezone_name = request.session.get('timezone', 'US/Eastern')
    return timezone(user_timezone_name)

def upcoming_events(request):
    # View function to display a list of upcoming events in Eastern Standard Time.
    est_timezone = get_est_timezone(request)
    current_time = now().astimezone(est_timezone)
    upcoming_events = Event.objects.filter(event_time__gt=str(current_time)).order_by('event_time')

    # Serialize the events into JSON format
    events_list = [{
        'id': event.id,
        'event_name': event.event_name,
        'event_location': event.event_location,
        'event_time': event.event_time,
        'general_admission_price': event.general_admission_price,
        'vip_ticket_price': event.vip_ticket_price,
        'event_image_url': event.event_image_url,
        'description': event.description
    } for event in upcoming_events]


    if not events_list:
        return JsonResponse({'events': [], 'message': 'No upcoming events found'})

    return JsonResponse({'events': events_list[10:35]})


@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        try:
            # data = json.loads(request.body)
            venue_user_email = request.POST.get('venueUserEmail')
            event_name = request.POST.get('eventName')
            event_time = request.POST.get('eventTime')
            event_location = request.POST.get('eventLocation')
            # event_image_url = data.get('eventImage')
            available_general_admission_tickets = int(request.POST.get('availGATix', 0))
            general_admission_price = float(request.POST.get('gaPrice', 0))
            available_vip_tickets = int(request.POST.get('availVipTix', 0))
            vip_ticket_price = float(request.POST.get('vipPrice', 0))
            genre = request.POST.get('eventGenre')
            description = request.POST.get('eventDescription')

            event_image_url = request.FILES.get('eventImage', None)

            if event_image_url:
                # generate unique file name
                file_name = f"{uuid.uuid4()}{event_image_url.name}"
                # s33 upload logic
                s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
                s3_client.upload_fileobj(event_image_url, settings.AWS_STORAGE_BUCKET_NAME, file_name)
                event_image_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_name}"
            else:
                event_image_url = None

            # Validate received data
            if not all([venue_user_email, event_name, event_time, event_location, event_image_url, genre, description]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # Create the event
            event = Event.objects.create(
                venue_user_email=venue_user_email,
                event_name=event_name,
                event_time=event_time,
                event_location=event_location,
                event_image_url=event_image_url,
                available_general_admission_tickets=available_general_admission_tickets,
                general_admission_price=general_admission_price,
                available_vip_tickets=available_vip_tickets,
                vip_ticket_price=vip_ticket_price,
                genre=genre,
                description=description
            )
            return JsonResponse({'message': 'Event created successfully!', 'id': event.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid data types provided'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def update_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)

    if request.method == 'POST':
        data = json.loads(request.body)
        venue_user_email = data.get('venue_user_email', event.venue_user_email)
        event_name = data.get('event_name', event.event_name)
        event_time = data.get('event_time', event.event_time)
        event_location = data.get('event_location', event.event_location)
        event_image_url = data.get('event_image_url', event.event_image_url)
        available_general_admission_tickets = data.get('available_general_admission_tickets',
                                                       event.available_general_admission_tickets)
        general_admission_price = data.get('general_admission_price', event.general_admission_price)
        available_vip_tickets = data.get('available_vip_tickets', event.available_vip_tickets)
        vip_ticket_price = data.get('vip_ticket_price', event.vip_ticket_price)
        genre = data.get('genre', event.genre)
        description = data.get('description', event.description)

        # Update the event
        event.venue_user_email = venue_user_email
        event.event_name = event_name
        event.event_time = event_time
        event.event_location = event_location
        event.event_image_url = event_image_url
        event.available_general_admission_tickets = available_general_admission_tickets
        event.general_admission_price = general_admission_price
        event.available_vip_tickets = available_vip_tickets
        event.vip_ticket_price = vip_ticket_price
        event.genre = genre
        event.description = description
        event.save()

        return JsonResponse({'message': 'Event updated successfully!'}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def get_venue_user(request):
    # Assume email is provided as a query parameter or part of the POST data
    email = request.GET.get('email') or request.POST.get('email')
    
    if email:
        try:
            # Retrieve the VenueUser by email
            user = VenueUser.objects.get(email=email)
            return user
        except ObjectDoesNotExist:
            # Handle the case where no user with this email exists
            # For now, return None, but you might want to handle this differently
            return None
    else:
        # Handle the case where no email is provided in the request
        # For now, return None, but you might want to handle this differently
        return None

def delete_event(request, event_id):
    if request.method == 'GET':
        try:
            event= Event.objects.filter(id=event_id)
            event.delete()
            return JsonResponse({'success': f'Event with id {event_id} deleted successfully'})
        except Event.DoesNotExist:
            return JsonResponse({'error': f'Event with id {event_id} does not exist'}, status=404)

@csrf_exempt
def get_events(request):
    # View function to get all events.
    if request.method == 'GET':
        events = Event.objects.all()
        events_list = [
            {   "id": event.id,
                "venue_user_email": event.venue_user_email,
                "event_name": event.event_name,
                "event_time": event.event_time,
                "event_location": event.event_location,
                "event_image_url": event.event_image_url,
                "available_general_admission_tickets": event.available_general_admission_tickets,
                "general_admission_price": event.general_admission_price,
                "available_vip_tickets": event.available_vip_tickets,
                "vip_ticket_price": event.vip_ticket_price,
                "genre": event.genre,
                "description": event.description
            }
            for event in events
        ]
        return JsonResponse({"events": events_list})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def search_events(request):
    event_name = request.GET.get('q', '')
    event_location = request.GET.get('eventLocation', '')

    if event_name and event_location:
        events = Event.objects.filter(event_name__icontains=event_name, event_location__icontains=event_location)
    elif event_name:
        events = Event.objects.filter(event_name__icontains=event_name)
    elif event_location:
        events = Event.objects.filter(event_location__icontains=event_location)
    else:
        events = Event.objects.none()

    # Serialize the queryset to JSON
    data = serializers.serialize('json', events)
    # Convert the JSON string to a Python list
    data = json.loads(data)
    return JsonResponse(data, safe=False)
