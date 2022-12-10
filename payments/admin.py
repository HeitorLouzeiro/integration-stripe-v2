from django.contrib import admin

from .models import Price, Product

# Register your models here.


class PriceInline(admin.TabularInline):
    model = Price
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [PriceInline]


admin.site.register(Product, ProductAdmin)
