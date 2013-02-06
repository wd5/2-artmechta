# -*- coding: utf-8 -*-
from django.contrib import admin
from apps.orders.models import  CartProduct,Order,OrderProduct

class CartProductInlines(admin.TabularInline):
    model = CartProduct
    readonly_fields = ('product',)
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ('id','create_date','sessionid',)
    list_display_links = ('id','create_date','sessionid',)
    list_filter = ('create_date',)
    inlines = [CartProductInlines,]

class OrderProductInlines(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('product','count',)
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','create_date','fullname','admin_summary',)
    list_display_links = ('id','fullname','create_date',)
    search_fields = ('fullname','email','phone','address','note','total_price',)
    list_filter = ('create_date','order_status',)
    readonly_fields = ('create_date',)
    inlines = [OrderProductInlines]

#admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)

