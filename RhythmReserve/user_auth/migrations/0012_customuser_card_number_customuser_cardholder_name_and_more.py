# Generated by Django 5.0.2 on 2024-03-28 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0011_alter_customuser_spotifyusername'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='card_number',
            field=models.CharField(blank=True, default=None, max_length=16, null=True, verbose_name='card number'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='cardholder_name',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='cardholder name'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='cvv',
            field=models.CharField(blank=True, default=None, max_length=3, null=True, verbose_name='CVV'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='exp_month',
            field=models.CharField(blank=True, default=None, max_length=2, null=True, verbose_name='expiration month'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='exp_year',
            field=models.CharField(blank=True, default=None, max_length=4, null=True, verbose_name='expiration year'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='zip_code',
            field=models.CharField(blank=True, default=None, max_length=10, null=True, verbose_name='zip code'),
        ),
    ]
