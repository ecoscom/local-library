# Generated by Django 3.0.3 on 2020-04-26 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app04', '0007_auto_20200401_1237'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name', 'first_name'], 'permissions': (('can_edit_author', 'Edit, update and delete Author'),)},
        ),
    ]
