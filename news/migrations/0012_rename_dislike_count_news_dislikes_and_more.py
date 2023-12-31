# Generated by Django 4.2.3 on 2023-08-05 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_remove_news_like_count_news_like_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='dislike_count',
            new_name='dislikes',
        ),
        migrations.RenameField(
            model_name='news',
            old_name='like_count',
            new_name='likes',
        ),
        migrations.AddField(
            model_name='news',
            name='editors_pick',
            field=models.BooleanField(default=False),
        ),
    ]
