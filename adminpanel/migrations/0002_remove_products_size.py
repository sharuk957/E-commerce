# Generated by Django 3.2.6 on 2021-09-11 02:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='size',
        ),
    ]
