# Generated by Django 5.0.4 on 2024-04-13 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_is_oauth'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='expiration_2fa',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
