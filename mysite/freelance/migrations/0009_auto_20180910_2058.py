# Generated by Django 2.0.5 on 2018-09-10 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelance', '0008_writer_urlhash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='Accepted_status',
            field=models.CharField(choices=[(1, 'Yes'), (2, 'No')], default=2, max_length=3),
        ),
    ]
