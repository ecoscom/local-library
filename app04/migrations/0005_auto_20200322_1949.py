# Generated by Django 3.0.3 on 2020-03-22 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app04', '0004_auto_20200217_2148'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='sumary',
            new_name='summary',
        ),
    ]