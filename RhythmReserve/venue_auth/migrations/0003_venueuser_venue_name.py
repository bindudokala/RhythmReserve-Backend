# Generated by Django 5.0.2 on 2024-03-07 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue_auth', '0002_remove_venueuser_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='venueuser',
            name='venue_name',
            field=models.CharField(default='joe', max_length=255),
            preserve_default=False,
        ),
    ]
