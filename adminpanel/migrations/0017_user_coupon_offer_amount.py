# Generated by Django 3.2.6 on 2021-10-07 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0016_user_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_coupon',
            name='offer_amount',
            field=models.IntegerField(default=200),
            preserve_default=False,
        ),
    ]
