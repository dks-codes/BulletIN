from django.db import models
from django.contrib.auth.models import User
from news.models import Plan

class Order(models.Model):
    user = models.ForeignKey(User, on_delete= models.DO_NOTHING)
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add= True)
    razor_pay_order_id = models.CharField(max_length= 100, null = True, blank=True)
    razor_pay_payment_id = models.CharField(max_length= 100, null = True, blank=True)
    razor_pay_payment_signature = models.CharField(max_length= 100, null = True, blank=True)
    paid = models.BooleanField(default=False)

# Create your models here.
