from django.contrib import admin

from .models import Category, Order, OrderItem, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "stock", "featured"]
    list_filter = ["category", "featured"]
    list_editable = ["price", "stock", "featured"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name", "description"]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product_name", "price", "quantity", "subtotal"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "email", "status", "total", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["full_name", "email"]
    readonly_fields = ["total", "created_at"]
    inlines = [OrderItemInline]
