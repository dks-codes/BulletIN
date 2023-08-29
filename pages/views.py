from django.shortcuts import render, HttpResponse, redirect
from news.models import News, NewsType, Plan, PlanFeatures
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings
from user.models import Order
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string 
from django.utils.html import strip_tags
from django.core.mail import send_mail


# Create your views here.
def index(request):
    '''Sends news data section wise to the index page and renders it'''
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
    # print(most_liked_id)
    most_liked = News.objects.filter(id__in = most_liked_id)[:4]
    # print(most_liked)
    # print(most_liked.query)

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
    '''Renders about us page'''
    return render(request, 'pages_temp/about.html')

def search(request):
    '''Helps in searching news'''
    if request.method == "POST":
        search = request.POST.get("search")
        news = News.objects.filter(Q(headline__icontains = search) | Q(cover_text__icontains = search) | Q(content__icontains = search) )
        context = {
            "search" : search,
            "news" : news
        }
    return render(request, 'pages_temp/search.html', context)

def subscribe(request):
    '''Renders the Subscription page to choose a plan'''
    plans = Plan.objects.all()
    features = PlanFeatures.objects.all()
    context = {
        "plans" : plans,
        "features" : features,
    }
    return render(request, 'pages_temp/subscribe.html', context)


@login_required(login_url = "/user/signin")
def order_summary(request):
    '''Renders order_summary page and the payment gateway to make payment'''
    if request.method == "POST":
        user = request.user
        plan_id = request.POST.get("plan_id")
        plans = Plan.objects.filter(id = plan_id)
        features = PlanFeatures.objects.all()
        for plan in plans:
            price = int(plan.price)
         
        client = razorpay.Client(auth= (settings.RAZOR_PAY_KEY_ID , settings.KEY_SECRET))
        payment = client.order.create({ 'amount': price * 100, 'currency':'INR', 'payment_capture':1 })
        # print(payment)

        request.session['sub'] = {'plan_id': plan_id, 'price':price}
        context = {
            "plans" : plans,
            "features" : features,
            "payment" : payment,
            "user" : user
        }
    
    return render(request,'pages_temp/order_summary.html',context)

@login_required(login_url = "/user/signin")
@csrf_exempt
def success(request):
    '''Receives order_id, payment_id, siganture from order_summary page and renders success page. Also, saves order details in Order table and sends an email to user'''
    if request.method == "POST":
        data = request.POST
        plan_id = request.session.get('sub')['plan_id']
        price = request.session.get('sub')['price']
        plan = Plan.objects.get(id = plan_id)

        client = razorpay.Client(auth= (settings.RAZOR_PAY_KEY_ID , settings.KEY_SECRET))
        status_dict = {'razorpay_order_id': data['razorpay_order_id'],
                       'razorpay_payment_id': data['razorpay_payment_id'],
                       'razorpay_signature': data['razorpay_signature']
        }
        # print(status_dict)
        try:
            status = client.utility.verify_payment_signature(status_dict)       #return True or False
            order = Order(
                user = request.user,
                plan = plan,
                price = float(price),
                razor_pay_order_id = data['razorpay_order_id'],
                razor_pay_payment_id =  data['razorpay_payment_id'],
                razor_pay_payment_signature = data['razorpay_signature'],
                paid = True
            )
            order.save()

            #EMAIL
            mail_context = {
                "username"  : request.user.first_name+" "+request.user.last_name,
                "plan" : plan,
                "price" : price
            }
            subject = "Successful Purchase"
            html_message = render_to_string('user/mail_template.html',mail_context)
            plain_message = strip_tags(html_message)
            to = [request.user.email,]
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject = subject, message= plain_message, from_email= from_email, recipient_list= to, fail_silently= False, html_message= html_message)

            return render(request, 'pages_temp/success.html', {'status' : True})
        except:
            return render(request, 'pages_temp/success.html', {'status' : False})


