# Generated by Django 5.0.2 on 2024-04-21 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0007_alter_payment_ticket_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='event_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='payment',
            name='event_time',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
