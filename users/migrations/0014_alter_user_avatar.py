# Generated by Django 5.0.4 on 2024-09-16 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='svg/profile_icon.svg', null=True, upload_to='avatars/'),
        ),
    ]