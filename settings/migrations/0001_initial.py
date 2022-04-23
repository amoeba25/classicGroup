# Generated by Django 4.0.4 on 2022-04-22 12:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('regionName', models.CharField(choices=[('North', 'North Zone'), ('East', 'East Zone'), ('West', 'West Zone'), ('South', 'South Zone')], max_length=10)),
                ('stateName', models.CharField(max_length=20, null=True)),
                ('cityName', models.CharField(max_length=20, null=True)),
                ('branchCode', models.CharField(max_length=10, null=True)),
                ('branchName', models.CharField(max_length=100, null=True)),
                ('branchAddress1', models.CharField(max_length=100, null=True)),
                ('branchAddress2', models.CharField(max_length=100, null=True)),
                ('zip_code', models.IntegerField(blank=True, null=True)),
                ('branchNumber', models.CharField(max_length=100, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, default='0', max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, default='0', max_digits=9, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Branch',
            },
        ),
        migrations.CreateModel(
            name='MapConfig',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('google_map_api', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Google Map API Key',
            },
        ),
    ]