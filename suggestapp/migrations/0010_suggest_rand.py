# Generated by Django 2.0 on 2020-06-21 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suggestapp', '0009_remove_suggest_rand'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggest',
            name='rand',
            field=models.IntegerField(default=0),
        ),
    ]
