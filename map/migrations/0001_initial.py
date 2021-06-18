# Generated by Django 3.2.4 on 2021-06-14 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BikeStation',
            fields=[
                ('bk_id', models.IntegerField(primary_key=True, serialize=False)),
                ('bk_contract_name', models.CharField(max_length=45)),
                ('bk_name', models.CharField(max_length=45)),
                ('bk_address', models.CharField(max_length=45)),
                ('bk_lat', models.FloatField()),
                ('bk_lng', models.FloatField()),
                ('bk_banking', models.CharField(max_length=45)),
                ('bk_bouns', models.CharField(max_length=45)),
                ('bk_bike_stands', models.IntegerField()),
                ('bk_available_bike_stands', models.IntegerField()),
                ('bk_available_bikes', models.IntegerField()),
                ('bk_status', models.CharField(max_length=45)),
                ('bk_last_update', models.CharField(max_length=45)),
            ],
        ),
    ]