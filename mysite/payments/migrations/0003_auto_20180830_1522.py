# Generated by Django 2.0.5 on 2018-08-30 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20180830_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='Amount',
            field=models.FloatField(default=0.0, max_length=255),
        ),
        migrations.AlterField(
            model_name='payment',
            name='email',
            field=models.EmailField(default='user.email.ac.ke', max_length=254),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user_id',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
