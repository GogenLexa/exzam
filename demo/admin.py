from django.contrib import admin

# Register your models here.
from demo.forms import OrderForm
from demo.models import *


class ItemInOrder(admin.TabularInline):
    model = ItemInOrder


class AdminOrder(admin.ModelAdmin):
    form = OrderForm
    list_filter = ('status',)
    list_display = ('user', 'date', 'count_product')
    fields = ('user', 'status', 'rejection_reason')
    inlines = (ItemInOrder,)


admin.site.register(Order, AdminOrder)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(User)
