# Generated by Django 2.0 on 2020-05-27 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycarapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mycar',
            name='about',
            field=models.TextField(default='-'),
        ),
    ]
