# Generated by Django 3.1.1 on 2020-09-29 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu_cards", "0003_auto_20200925_1435"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dish",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
