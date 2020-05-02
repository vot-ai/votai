# Generated by Django 3.0.5 on 2020-05-02 19:17

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('active', models.BooleanField(default=False)),
                ('prioritized', models.BooleanField(default=False)),
                ('mu', models.FloatField(default=0.0)),
                ('sigma_squared', models.FloatField(default=1.0)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='surveys.Survey')),
            ],
        ),
    ]
