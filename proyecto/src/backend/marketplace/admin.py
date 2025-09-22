from django.contrib import admin
from .models import Category, Product, ProductImage, Transaction, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'category', 'price', 'condition', 'status', 'views', 'created_at']
    list_filter = ['category', 'condition', 'status', 'created_at']
    search_fields = ['title', 'description', 'seller__username']
    readonly_fields = ['views', 'created_at', 'updated_at']
    raw_id_fields = ['seller']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    raw_id_fields = ['product']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['product', 'buyer', 'seller', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['product__title', 'buyer__username', 'seller__username']
    raw_id_fields = ['product', 'buyer', 'seller']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewed_user', 'reviewer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['reviewed_user__username', 'reviewer__username']
    raw_id_fields = ['transaction', 'reviewer', 'reviewed_user']