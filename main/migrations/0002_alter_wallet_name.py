# Generated by Django 4.1.5 on 2023-02-06 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wallet",
            name="name",
            field=models.CharField(default="836720C4", max_length=8, unique=True),
        ),
    ]
