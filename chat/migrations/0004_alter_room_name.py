# Generated by Django 5.0.4 on 2024-04-13 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_room_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
