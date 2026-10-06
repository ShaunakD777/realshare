from django.contrib import admin
from .models import SellerProfile

@admin.action(description="Approve selected sellers")
def approve_sellers(modeladmin, request, queryset):
    queryset.update(is_approved=True)

class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_approved')
    actions = [approve_sellers]

admin.site.register(SellerProfile, SellerProfileAdmin)
