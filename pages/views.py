from django.shortcuts import render, HttpResponse
from news.models import News, NewsType, Plan, PlanFeatures
from django.db.models import Q


# Create your views here.
def index(request):
    # news1 =  News.objects.filter(news_option = ("CN",)).order_by('?')[:3]
    news1 =  News.objects.filter(news_type = NewsType.objects.get(type = "Carousel News")).order_by('?')[:3]
    news2 = News.objects.filter(news_type = NewsType.objects.get(type = "Breaking News")).order_by('?')[:4]
    news3 = News.objects.filter(news_type = NewsType.objects.get(type = "Editors' Pick")).order_by('?')[:4]

    all_news = News.objects.all()
    likes = {}
    for n in all_news:
        likes[n.pk] = n.total_likes()
    # print(likes)
    most_liked_id = dict(sorted(likes.items(), key= lambda x: x[1], reverse=True))
    print(most_liked_id)
    most_liked = News.objects.filter(id__in = most_liked_id)[:4]
    print(most_liked)
    print(most_liked.query)

    # news = News.objects.all()[:4]
    news = News.objects.all().exclude(id__in = news1.values_list('id',flat=True)).order_by('?')[:4]

    context = {
        "carousel_news" : news1,
        "breaking_news" : news2,
        "editors_pick" : news3,
        "most_liked" : most_liked,
        "news" : news,
    }
    return render(request, 'pages_temp/index.html', context)

def aboutus(request):
    return render(request, 'pages_temp/about.html')

def search(request):
    if request.method == "POST":
        search = request.POST.get("search")
        news = News.objects.filter(Q(headline__icontains = search) | Q(cover_text__icontains = search) | Q(content__icontains = search) )
        context = {
            "search" : search,
            "news" : news
        }
    return render(request, 'pages_temp/search.html', context)

def subscribe(request):
    plans = Plan.objects.all()
    features = PlanFeatures.objects.all()
    context = {
        "plans" : plans,
        "features" : features,
    }
    return render(request, 'pages_temp/subscribe.html', context)

def payment(request):
    if request.method == "POST":
        plan_id = request.POST.get("plan.id")
    return render(request,'pages_temp/payment.html')
