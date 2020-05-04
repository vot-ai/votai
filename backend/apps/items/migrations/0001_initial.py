# Generated by Django 3.0.5 on 2020-05-04 01:42

import backend.fields
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
                ('uuid', backend.fields.ShortUUIDField(auto_created=True, default=backend.fields.default_gen, editable=False, max_length=7, unique=True)),
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
