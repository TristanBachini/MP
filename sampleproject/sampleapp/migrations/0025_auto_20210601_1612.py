# Generated by Django 3.1.7 on 2021-06-01 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0024_auto_20210601_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcard',
            name='cardnumber',
            field=models.BigIntegerField(null=True),
        ),
    ]