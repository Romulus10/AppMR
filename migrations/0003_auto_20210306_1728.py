# pylint: skip-file
# Generated by Django 3.1.7 on 2021-03-06 22:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("appMR", "0002_supportticket_active"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="text",
            new_name="content",
        ),
    ]
