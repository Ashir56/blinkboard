# Generated by Django 5.0.1 on 2024-01-28 02:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0009_delete_friendrequest"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Friend",
        ),
    ]