# Generated by Django 5.0.2 on 2024-02-28 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('user_auth', '0006_alter_customuser_spotifyusername_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='customuser_groups', related_query_name='customuser', to='auth.group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='customuser_permissions', related_query_name='customuser', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
