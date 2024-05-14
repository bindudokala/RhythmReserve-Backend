from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
import json

@csrf_exempt
def edit_profile(request):
    User = get_user_model()  # Get the custom user model

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))  # Load the JSON data from request
            email = data.get('email')  # Assuming the email is used to identify the user

            # Ensure email is provided
            if not email:
                return JsonResponse({'error': 'Email is required'}, status=400)

            # Find the user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

            print(data)
            
            # Update user fields
            user.username = data.get('username', user.username)
            user.spotifyUsername = data.get('spotifyUsername', user.spotifyUsername)
            user.phoneNumber = data.get('phoneNumber', user.phoneNumber)
            user.cardholder_name = data.get('cardHolderName', user.cardholder_name)
            user.card_number = data.get('cardNumber', user.card_number)
            user.exp_month = data.get('expMonth', user.exp_month)
            user.exp_year = data.get('expYear', user.exp_year)
            user.cvv = data.get('cvv', user.cvv)
            user.zip_code = data.get('zipCode', user.zip_code)
            

            user.save()  # Save the updated user object

            # Prepare and send the updated user data as response
            response_data = {
                'firstName': user.first_name,
                'lastName': user.last_name,
                'email': user.email,
                'username': user.username,
                'spotifyUsername': user.spotifyUsername,
                'phoneNumber': user.phoneNumber,
                'cardNumber': user.card_number,
                'cardHolderName': user.cardholder_name,
                'expMonth': user.exp_month,
                'expYear': user.exp_year,
                'cvv': user.cvv,
                'zipCode': user.zip_code
            }
            return JsonResponse(response_data, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)