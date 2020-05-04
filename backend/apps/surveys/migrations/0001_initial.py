# Generated by Django 3.0.5 on 2020-05-04 01:42

import backend.fields
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', backend.fields.ShortUUIDField(auto_created=True, default=backend.fields.default_gen, editable=False, max_length=7, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('max_time', models.PositiveSmallIntegerField(default=600)),
                ('min_views', models.PositiveSmallIntegerField(default=5)),
                ('allow_concurrent', models.BooleanField(default=True)),
                ('max_annotators', models.PositiveIntegerField(default=50)),
                ('max_items', models.PositiveIntegerField(default=100)),
                ('gamma', models.FloatField(default=5.0)),
                ('epsilon', models.FloatField(default=0.25)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='surveys', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
