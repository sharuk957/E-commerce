# Generated by Django 3.2.6 on 2021-09-11 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0003_auto_20210911_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.IntegerField(blank=True),
        ),
    ]
