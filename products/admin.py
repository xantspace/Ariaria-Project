from django.contrib import admin
from .models import Category, Product, SellerInventory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'category', 'price', 'stock_quantity', 'is_active')
    list_filter = ('category', 'is_active', 'is_verified')
    search_fields = ('name', 'seller__first_name')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SellerInventory)
class SellerInventoryAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "seller",
        "available_quantity",
        "low_stock_threshold",
        "is_listed",
        "created_at",
    )
    list_filter = ("is_listed",)
    search_fields = ("product__name", "seller__email")
    ordering = ("-created_at",)