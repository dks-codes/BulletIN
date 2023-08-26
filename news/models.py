from django.db import models
from django.contrib.auth.models import User

from multiselectfield import MultiSelectField

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category


class NewsType(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type


class News(models.Model):
    # NEWS_OPTION = [
    #     ("NN","Normal News"),
    #     ("BN","Breaking News"),
    #     ("EP","Editors' Pick"),
    #     ("F","Features"),
    #     ("CN","Carousel News"),
    #     ("CaN","Card News")
    # ]

    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    headline = models.CharField(max_length=255, blank=True)
    report_by = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    likes = models.ManyToManyField(User,blank=True)
    dislikes = models.IntegerField(default=0)
    cover_photo = models.ImageField(upload_to="news_cover_images", blank=True)
    cover_text = models.CharField(max_length=255, blank=True)
    # news_option = MultiSelectField(max_length=40, choices = NEWS_OPTION, default= "NN")
    news_type = models.ManyToManyField(NewsType,blank=True)

    class Meta:
        verbose_name_plural = "News"
        ordering = ['-date']

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.headline
    
class Comment(models.Model):
    news = models.ForeignKey(News, on_delete = models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.user.username + ' - ' + self.comment
    
class PlanFeatures(models.Model):
    feature = models.CharField(max_length = 255)

    def __str__(self):
        return self.feature
    class Meta:
        verbose_name_plural = "Plan Features"

class Plan(models.Model):
    plan_name = models.CharField(max_length= 255)
    price = models.FloatField()
    feature = models.ManyToManyField(PlanFeatures,blank=True)

    def __str__(self):
        return self.plan_name
    
    class Meta:
        verbose_name_plural = "Plans"

 

    