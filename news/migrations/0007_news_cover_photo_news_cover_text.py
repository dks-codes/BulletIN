# Generated by Django 4.2.3 on 2023-07-18 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_news_dislike_count_news_like_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='cover_photo',
            field=models.ImageField(blank=True, upload_to='news_cover_images'),
        ),
        migrations.AddField(
            model_name='news',
            name='cover_text',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
