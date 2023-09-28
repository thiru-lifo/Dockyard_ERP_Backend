from django.contrib import admin
from .models import IPL

# Register your models here.
class IPLAdmin(admin.ModelAdmin):

    list_display = ('team', 'captain', 'city')
    list_filter = ("team", "captain", "city")
    search_fields = ("team", "captain")
    
    
    fieldsets = (
        ('Standard info', {
            'fields': ('team', 'captain', 'city')
        }), )

admin.site.register(IPL, IPLAdmin)