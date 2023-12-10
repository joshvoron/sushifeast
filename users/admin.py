from django.contrib import admin

from .models import BasketItem, BasketModel, CustomUserModel, EmailVerification


class CustomUserModelAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email')
    list_display_links = ('first_name', 'last_name', 'username', 'email')
    search_fields = ('username', 'email',)


class BasketModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'creation_date',)
    list_display_links = ('user', 'creation_date',)
    search_fields = ('user', )


class BasketItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', )
    list_display_links = ('product', 'quantity', )
    search_fields = ('product', )


class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'expiration', )
    readonly_fields = ('created', )


admin.site.register(CustomUserModel, CustomUserModelAdmin)
admin.site.register(BasketModel, BasketModelAdmin)
admin.site.register(BasketItem, BasketItemAdmin)
admin.site.register(EmailVerification, EmailVerificationAdmin)
