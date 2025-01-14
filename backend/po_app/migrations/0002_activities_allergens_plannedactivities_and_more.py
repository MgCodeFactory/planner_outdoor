# Generated by Django 5.1.3 on 2025-01-14 18:05

import django.db.models.deletion
import django.utils.timezone
import po_app.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('po_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, validators=[po_app.validators.CustomNameValidator()])),
                ('description', models.CharField(max_length=200, unique=True, validators=[po_app.validators.CustomDescriptionValidator()])),
            ],
            options={
                'verbose_name_plural': 'Activities',
            },
        ),
        migrations.CreateModel(
            name='Allergens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, validators=[po_app.validators.CustomNameValidator()])),
                ('description', models.CharField(max_length=200, unique=True, validators=[po_app.validators.CustomDescriptionValidator()])),
            ],
            options={
                'verbose_name_plural': 'Allergens',
            },
        ),
        migrations.CreateModel(
            name='PlannedActivities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.JSONField(validators=[po_app.validators.CustomLocationValidator()])),
                ('start_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='po_app.activities')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'PlannedActivities',
                'unique_together': {('user', 'activity', 'start_datetime', 'end_datetime')},
            },
        ),
        migrations.CreateModel(
            name='UserActivities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='po_app.activities')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'UserActivities',
                'unique_together': {('user', 'activity')},
            },
        ),
        migrations.CreateModel(
            name='UserAllergens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allergen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='po_app.allergens')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'UserAllergens',
                'unique_together': {('user', 'allergen')},
            },
        ),
    ]
