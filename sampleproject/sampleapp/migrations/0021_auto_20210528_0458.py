# Generated by Django 3.1.7 on 2021-05-28 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0020_purchasechoice_purchasechoices'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PurchaseChoices',
            new_name='PurchaseSelect',
        ),
    ]