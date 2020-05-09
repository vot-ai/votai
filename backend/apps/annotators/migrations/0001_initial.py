# Generated by Django 3.0.5 on 2020-05-09 18:55

import backend.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('surveys', '0001_initial'),
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annotator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', backend.fields.ShortUUIDField(auto_created=True, blank=True, default=backend.fields.default_gen, editable=False, max_length=22, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('active', models.BooleanField(default=True)),
                ('alpha', models.FloatField(default=10)),
                ('beta', models.FloatField(default=1)),
                ('current', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_annotators', to='items.Item')),
                ('ignored', models.ManyToManyField(related_name='ignored_by', to='items.Item')),
                ('previous', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous_annotators', to='items.Item')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annotators', to='surveys.Survey')),
                ('viewed', models.ManyToManyField(related_name='viewed_by', to='items.Item')),
            ],
        ),
    ]
