# Generated by Django 3.0.3 on 2020-02-16 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app04', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Linguagem do livro', max_length=200)),
            ],
        ),
    ]