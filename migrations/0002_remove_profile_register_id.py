# Generated by Django 2.1.2 on 2018-12-17 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chahana', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='register_id',
        ),
    ]