# Generated by Django 5.0.2 on 2024-02-25 00:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0005_alter_customuser_spotifyusername'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='spotifyUsername',
            field=models.CharField(blank=True, default='', max_length=31, verbose_name='spotfify username'),
        ),
        migrations.CreateModel(
            name='PasswordResetRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reset_code', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='password_reset_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
