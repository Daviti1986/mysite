# Generated by Django 2.0 on 2020-06-11 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycarapp', '0010_auto_20200611_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='mycar',
            name='picname2',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='mycar',
            name='picurl2',
            field=models.TextField(default=''),
        ),
    ]
