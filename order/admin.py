from django.contrib import admin
from nested_inline.admin import NestedStackedInline,NestedModelAdmin
from .models import *

class OrderItemInline(NestedStackedInline):
    model = OrderItem
    extra = 0

class OrderAdmin(NestedModelAdmin):
    list_display = ('id','phone','is_paid','is_done','is_deliveried','total_price','created_at',)
    model = Order
    inlines = [OrderItemInline]
    list_filter = ('is_paid','is_done','is_deliveried',)
    readonly_fields = ['total_price']

    def total_price(self, obj):
        return obj.total_price

    total_price.short_description = 'Сумма заказа'

admin.site.register(Order,OrderAdmin)
admin.site.register(Delivery)
admin.site.register(Payment)

