# Generated by Django 2.0.5 on 2018-08-30 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0008_auto_20180830_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='username',
            field=models.CharField(default='kenny', max_length=30),
        ),
    ]
