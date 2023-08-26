# Generated by Django 4.2.3 on 2023-08-07 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0014_newstype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='news_option',
        ),
        migrations.AddField(
            model_name='news',
            name='news_type',
            field=models.ManyToManyField(blank=True, to='news.newstype'),
        ),
    ]
