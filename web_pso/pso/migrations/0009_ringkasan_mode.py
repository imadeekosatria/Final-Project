# Generated by Django 4.0.5 on 2022-12-06 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pso', '0008_alter_berita_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='ringkasan',
            name='mode',
            field=models.CharField(default='pso', max_length=255),
        ),
    ]