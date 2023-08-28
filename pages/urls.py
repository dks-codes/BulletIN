from django.urls import path
from pages import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about",views.aboutus, name="aboutus"),
    path("search", views.search, name= "search"),
    path("subscribe", views.subscribe, name= "subscribe"),
    # path("buy_now", views.buy_now, name= "buy_now"),
    path("ordersummary", views.order_summary, name="order_summary"),
    path("success", views.success, name="success"),
    # path("payment", views.payment, name="payment")


]
