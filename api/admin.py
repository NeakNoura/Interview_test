from django.contrib import admin
from .models import ProductTB, CategoryTB


class ProductTBAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')


admin.site.register(ProductTB, ProductTBAdmin)
admin.site.register(CategoryTB)
