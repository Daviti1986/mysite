# Generated by Django 2.0 on 2020-05-27 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycarapp', '0002_mycar_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mycar',
            name='about',
            field=models.TextField(),
        ),
    ]
