# Generated by Django 2.0 on 2020-06-22 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CommentApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
