# Generated by Django 4.2.7 on 2023-11-19 14:52

from django.db import migrations
import users.managers


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_user_last_login'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', users.managers.AsyncUserManager()),
            ],
        ),
    ]