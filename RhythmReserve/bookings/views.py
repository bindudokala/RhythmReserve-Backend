from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Payment
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import json
import sendgrid
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
import ssl
import uuid

ssl._create_default_https_context = ssl._create_stdlib_context

User = get_user_model()


@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        # Assuming the user is authenticated; you may need to adjust this depending on your authentication setup

        data = json.loads(request.body)
        event_name = data.get('event_name')
        event_time = data.get('event_time')
        amount = data.get('amount')
        user_email=data.get('user_email')
        ticket_type=data.get('type')
        print("data",data)
        print("user",user_email)

        # Fetch the user object from the database using the user_id
        try:
            user_details = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found.'}, status=404)

        t=str(uuid.uuid4())
        # Mocking a payment response as if it were from a payment gateway
        # In real scenarios, replace this with an actual API call to your payment gateway
        response_data = {
            'successful': True,  # Simulate a successful transaction
            'transaction_id': t,
            'event_name': event_name,
            'event_time': event_time,
            'ticket_type': ticket_type,
            'amount': amount
        }

        status = 'Success' if response_data.get('successful') else 'Failed'
        transaction_id = t

        # Save the payment details in your database
        payment = Payment.objects.create(user=user_details.id, ticket_type=ticket_type, event_name=event_name, event_time=event_time, amount=amount, status=status, transaction_id=transaction_id)

        # If payment is successful, send an email
        if status == 'Success':
            sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
            from_email = 'ReserveRhythm@gmail.com'  # sendgrid email
            to_email = user_details.email
            subject = 'Payment Confirmation'
            content = f'Hi there, \n\nBelow is the payment confirmation.\n\nEvent Name: {event_name}\nEvent_time: {event_time}\nTicket Type: {ticket_type}\nTotal Amount: ${amount}\nYour transaction ID is {transaction_id}\n'
            mail = Mail(from_email, to_email, subject, content)
            response = sg.send(mail)

            return JsonResponse({
                'message': 'Payment successful and email sent.',
                'data': response_data
            }, status=200)

        return JsonResponse({'message': 'Payment failed.'}, status=400)