from django.contrib import admin
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category, CategoryAdmin)
