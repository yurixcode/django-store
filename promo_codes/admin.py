from django.contrib import admin

from .models import PromoCode

class PromoCodeAmin(admin.ModelAdmin):
    exclude = ['code']

admin.site.register(PromoCode, PromoCodeAmin)