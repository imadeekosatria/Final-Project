# Generated by Django 4.0.5 on 2022-11-30 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pso', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ringkasan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=255)),
                ('teks_asli', models.CharField(max_length=255)),
                ('ringkasan', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
