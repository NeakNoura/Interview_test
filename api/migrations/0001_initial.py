# Generated by Django 5.1.5 on 2025-01-24 14:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryTB',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ProductTB',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='products/')),
                ('price', models.FloatField()),
                ('cat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.categorytb')),
            ],
        ),
    ]
