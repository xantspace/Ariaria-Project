from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Order  

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('first_name','email', 'role', 'is_verified', 'date_joined')
    list_filter = ('role', 'is_verified', 'is_staff')
    search_fields = ('email', 'first_name', 'business_name')
    
    # If you added custom fields, add them to fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'phone_number', 'business_name', 'is_verified')}),
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'product')