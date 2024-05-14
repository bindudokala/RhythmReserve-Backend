# models.py

from django.db import models
from django.conf import settings

class Payment(models.Model):
    user = models.BigIntegerField()
    event_name = models.CharField(max_length=100, default="")
    event_time = models.CharField(max_length=255, default=None)
    ticket_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=255)

    # Add more fields as necessary

