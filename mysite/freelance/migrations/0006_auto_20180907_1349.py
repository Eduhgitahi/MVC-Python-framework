# Generated by Django 2.0.5 on 2018-09-07 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelance', '0005_auto_20180611_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='urlhash',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='Reference Number'),
        ),
    ]