# Generated by Django 5.0.2 on 2024-03-28 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='genre',
            field=models.CharField(max_length=60),
        ),
    ]
