# Generated by Django 3.2.5 on 2021-07-20 20:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated_at')),
                ('tour_name', models.CharField(max_length=255)),
                ('from_city', models.CharField(max_length=255)),
                ('to_city', models.CharField(max_length=255)),
                ('tour_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='tour date')),
                ('note', models.TextField(verbose_name='Tour Note')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]