# Generated by Django 5.0.4 on 2024-10-24 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_blockeduser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='png/profile_default.png', null=True, upload_to='avatars/'),
        ),
    ]
