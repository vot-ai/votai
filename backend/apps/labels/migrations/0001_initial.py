# Generated by Django 3.0.5 on 2020-05-02 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('annotators', '0001_initial'),
        ('items', '0001_initial'),
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('annotator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='labels', to='annotators.Annotator')),
                ('loser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loser_labels', to='items.Item')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='labels', to='surveys.Survey')),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winner_labels', to='items.Item')),
            ],
        ),
    ]
