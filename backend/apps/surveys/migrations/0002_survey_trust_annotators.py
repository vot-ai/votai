# Generated by Django 3.0.5 on 2020-05-09 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='trust_annotators',
            field=models.BooleanField(default=True),
        ),
    ]
