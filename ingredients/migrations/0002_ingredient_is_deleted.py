# Generated by Django 3.2.6 on 2021-08-24 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='is_deleted',
            field=models.BooleanField(default=0),
        ),
    ]
