# Generated by Django 2.0 on 2020-06-02 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suggestapp', '0002_auto_20200602_1335'),
    ]

    operations = [
        migrations.RenameField(
            model_name='suggest',
            old_name='pic',
            new_name='picname',
        ),
        migrations.AddField(
            model_name='suggest',
            name='picurl',
            field=models.TextField(default='-'),
        ),
    ]
