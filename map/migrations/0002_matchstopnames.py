# Generated by Django 3.2.4 on 2021-08-16 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchStopNames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stoppointid', models.IntegerField(blank=True, null=True)),
                ('stop_name', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'match_stop_names',
                'managed': False,
            },
        ),
    ]
