# Generated by Django 3.0.3 on 2020-08-20 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('batch_module', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='config',
            field=models.TextField(default='{}'),
        ),
    ]
