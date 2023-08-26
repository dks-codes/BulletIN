from django.urls import path
from pages import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about",views.aboutus, name="aboutus"),
    path("search", views.search, name= "search"),
    path("subscribe", views.subscribe, name= "subscribe"),
    path("payment", views.payment, name="payment")

]
