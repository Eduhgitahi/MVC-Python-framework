# Generated by Django 2.0.5 on 2018-08-30 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_auto_20180830_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='receiver',
            field=models.CharField(default='receiver', max_length=30),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='sender',
            field=models.CharField(default='user', max_length=30),
        ),
    ]
