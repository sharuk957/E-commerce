# Generated by Django 3.2.6 on 2021-09-14 08:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userlogin', '0007_alter_cart_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('country', models.CharField(max_length=250)),
                ('street_address', models.CharField(max_length=1500)),
                ('city', models.CharField(max_length=250)),
                ('state', models.CharField(max_length=250)),
                ('pin_code', models.IntegerField()),
                ('phn_no', models.IntegerField()),
                ('order_notes', models.CharField(max_length=2500, null=True)),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
