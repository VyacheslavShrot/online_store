# Generated by Django 4.1.7 on 2023-04-18 08:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={"verbose_name": "Order", "verbose_name_plural": "All Orders"},
        ),
    ]