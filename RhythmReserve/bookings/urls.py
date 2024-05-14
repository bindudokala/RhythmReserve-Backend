# urls.py

from django.urls import path
from . import views
from .views import process_payment

urlpatterns = [
    # Your other URL patterns...
    path("payment/", views.process_payment, name='process_payment'),
]
