# pylint: skip-file
# Generated by Django 3.2.8 on 2021-10-25 02:55

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_mr", "0011_supportticket_last_updated"),
    ]

    operations = [
        migrations.AlterField(
            model_name="supportticket",
            name="last_updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
