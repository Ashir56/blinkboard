# Generated by Django 5.0.1 on 2024-01-28 02:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0010_delete_friend"),
    ]

    operations = [
        migrations.CreateModel(
            name="Friend",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("Pending", "Pending"), ("Accepted", "Accepted")],
                        default="Pending",
                        max_length=20,
                    ),
                ),
                (
                    "friend",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="friendships_as_friend",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="friendships_as_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="friend",
            constraint=models.UniqueConstraint(
                fields=("user", "friend"), name="unique_friendship"
            ),
        ),
    ]