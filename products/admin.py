from django.contrib import admin

from .models import CategoryModel, ProductModel


class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'is_available', 'new', 'hit')
    list_display_links = ('title', 'category', 'price', 'is_available')
    search_fields = ('title', 'category',)


class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_display_links = ('title', )
    search_fields = ('title', )


admin.site.register(ProductModel, ProductModelAdmin)
admin.site.register(CategoryModel, CategoryModelAdmin)
