# Generated by Django 5.0.4 on 2024-09-10 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_user_email_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]