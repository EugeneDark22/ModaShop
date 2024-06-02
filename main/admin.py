from django.contrib import admin
from .models import Product, Order, ContactMessage

admin.site.register(Product)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_cost', 'address', 'created_at', 'is_processed']
    list_filter = ['is_processed', 'created_at']
    search_fields = ['user__username', 'total_cost', 'address']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'message']