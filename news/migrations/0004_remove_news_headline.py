# Generated by Django 4.2.3 on 2023-07-16 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_news_options_alter_news_headline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='headline',
        ),
    ]
