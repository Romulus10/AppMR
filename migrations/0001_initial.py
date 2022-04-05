# pylint: skip-file
# Generated by Django 3.1.7 on 2021-03-06 21:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=256)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SupportTicket",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=32)),
                ("description", models.CharField(max_length=256)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("1", "Waiting"),
                            ("2", "Seen"),
                            ("3", "Confirmed"),
                            ("4", "In Progress"),
                            ("5", "Resolved"),
                            ("6", "Verified"),
                        ],
                        max_length=32,
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now=True)),
                ("comments", models.ManyToManyField(to="app_mr.Comment")),
                (
                    "reporter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
