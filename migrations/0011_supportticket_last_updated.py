# pylint: skip-file
# Generated by Django 3.2.8 on 2021-10-25 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_mr", "0010_auto_20210830_1504"),
    ]

    operations = [
        migrations.AddField(
            model_name="supportticket",
            name="last_updated",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
