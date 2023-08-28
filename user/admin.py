from django.contrib import admin
from user.models import Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','plan','price','created_at','razor_pay_order_id']

admin.site.register(Order,OrderAdmin)

