# Generated by Django 2.0.7 on 2018-07-25 18:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 25, 18, 58, 31, 742353, tzinfo=utc), verbose_name='date published'),
        ),
    ]