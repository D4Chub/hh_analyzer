# Generated by Django 5.1.7 on 2025-03-06 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills_stats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='published_at',
            field=models.DateTimeField(verbose_name='Дата публикации'),
        ),
    ]
