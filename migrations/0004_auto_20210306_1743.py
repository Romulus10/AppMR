# pylint: skip-file
# Generated by Django 3.1.7 on 2021-03-06 22:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_mr", "0003_auto_20210306_1728"),
    ]

    operations = [
        migrations.AlterField(
            model_name="supportticket",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("1", "Waiting"),
                    ("2", "Seen"),
                    ("3", "Confirmed"),
                    ("4", "In Progress"),
                    ("5", "Resolved"),
                    ("6", "Verified"),
                ],
                max_length=32,
                null=True,
            ),
        ),
    ]
