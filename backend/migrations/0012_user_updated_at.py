# Generated by Django 5.0.1 on 2024-01-30 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0011_friend_friend_unique_friendship"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="updated_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
