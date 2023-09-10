from django.shortcuts import render, get_object_or_404, redirect
from news.models import News, Category, Comment
from django.contrib.auth.models import User

def all_news(request):
    news = News.objects.all().order_by('?')[:4]
    categories = Category.objects.exclude(category__in = ("Opinion","Photography")).order_by('category')
    print(categories.query)
    must_see = News.objects.all().order_by('?')[:3]
    most_read = News.objects.all().order_by('?')[:3]

    most_read_list = []
    count_most_read = len(most_read)
    for i in range(count_most_read):
        most_read_list.append(i)

    # count_cat = len(categories)
    # cat_list = []
    # for i in range(0,count_cat):
    #     cat_list.append(i)

    context = {
        "news" : news,
        "must_see" : must_see,
        "most_read" : most_read,
        "categories" : categories,
        "count" : most_read_list,
        # "count_cat" : count_cat,
    }
    return render(request, "news/news.html", context)

def news_category(request, cid):
    news1 = News.objects.filter(category = cid).order_by('?').first()
    news = News.objects.filter(category = cid).order_by('?')[1:4]
    categories = Category.objects.exclude(category__in = ("Opinion","Photography")).order_by('category')
    each_category = Category.objects.filter(id = cid)
    # must_see = News.objects.all().order_by('?')[:3]
    # most_read = News.objects.all().order_by('?')[:3]
    dict = {
        "news1" : news1,
        "news" : news,
        "categories" : categories,
        "each_category" : each_category
        # "must_see" : must_see,
        # "most_read" : most_read,
    }
    return render(request, 'news/news_category.html', dict)

def news_details(request, id):
    news = get_object_or_404(News,id = id)
    comments = Comment.objects.filter(news = news)

    flag = False

    if request.user.is_authenticated:
            user = request.user
            if news.likes.filter(id = user.id).exists():
                flag = True

    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user

            if news.likes.filter(id = user.id).exists():
                news.likes.remove(user)
                flag = False
            else:
                 news.likes.add(user)
                 flag = True

    context = {
        "news" : news,
        "comments" : comments,
        "flag" : flag
    }
    return render(request, 'news/news_details.html', context)


def add_comment(request, nid):
    if request.method == "POST":
        user = request.user
        # news_id = request.POST.get('news.id')
        news = News.objects.get( id = nid)
        comment = request.POST.get("comment")

        user_comment = None                            #user_comment is a variable created
        if user_comment is None:
            user_comment =  Comment()
            user_comment.user = user
            user_comment.news = news
            user_comment.comment = comment
            user_comment.save()
        return redirect('news_details', nid )