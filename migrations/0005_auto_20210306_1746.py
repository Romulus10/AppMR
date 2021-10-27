# Generated by Django 3.1.7 on 2021-03-06 22:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("appMR", "0004_auto_20210306_1743"),
    ]

    operations = [
        migrations.AlterField(
            model_name="supportticket",
            name="reporter",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
