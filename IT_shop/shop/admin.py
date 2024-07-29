from django.contrib import admin
# Register your models here.
from .models import *
class ProductAdmin(admin.ModelAdmin):
	prepopulated_fields={"slug":('name',)}
admin.site.register(Product, ProductAdmin)
class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields={"slug":('name',)}
admin.site.register(Category, CategoryAdmin)