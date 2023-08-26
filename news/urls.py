from django.urls import path
from news.views import all_news, news_category, news_details, add_comment

urlpatterns = [
    path("", all_news , name="all_news"),
    path("news_category/<int:cid>/", news_category, name="news_category"),
    path("<int:id>/", news_details, name="news_details"),
    path("add_comment/<int:nid>", add_comment, name="add_comment")
]
