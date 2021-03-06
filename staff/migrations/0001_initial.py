# Generated by Django 3.1.8 on 2022-05-27 03:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('linkedIn_link', models.CharField(blank=True, max_length=100, null=True)),
                ('aadhar_No', models.CharField(blank=True, max_length=30, null=True)),
                ('pan_card', models.CharField(blank=True, max_length=50, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Profile',
            },
        ),
    ]
