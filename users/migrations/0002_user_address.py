# Generated by Django 4.0.1 on 2022-01-09 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(default='a', max_length=255),
        ),
    ]
