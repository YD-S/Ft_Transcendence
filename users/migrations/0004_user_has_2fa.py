# Generated by Django 5.0.4 on 2024-04-11 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_2fa',
            field=models.BooleanField(default=False),
        ),
    ]
