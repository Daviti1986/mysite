# Generated by Django 2.0 on 2020-06-02 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suggestapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggest',
            name='catid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='suggest',
            name='catname',
            field=models.CharField(default='-', max_length=30),
        ),
        migrations.AddField(
            model_name='suggest',
            name='show',
            field=models.IntegerField(default=0),
        ),
    ]
