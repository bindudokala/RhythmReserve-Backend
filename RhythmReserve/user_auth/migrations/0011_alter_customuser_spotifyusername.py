# Generated by Django 5.0.2 on 2024-03-28 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0010_remove_customuser_card_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='spotifyUsername',
            field=models.CharField(blank=True, default='', max_length=31, verbose_name='spotify username'),
        ),
    ]
