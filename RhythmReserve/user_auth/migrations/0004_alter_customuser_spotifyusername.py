# Generated by Django 4.2.10 on 2024-02-22 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0003_alter_customuser_options_customuser_spotifyusername_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='spotifyUsername',
            field=models.CharField(max_length=15, unique=True, verbose_name='spotify username'),
        ),
    ]
