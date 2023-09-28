from django.contrib import admin
from .models import Notification

# Register your models here.
class NotificationAdmin(admin.ModelAdmin):

    list_display = ('title', 'message', 'type')
    list_filter = ("title", "type", "message")
    search_fields = ("title", "message")
    
    
    fieldsets = (
        ('Standard info', {
            'fields': ('title', 'type', 'subject', 'message', 'to', 'cc','bcc', 'attachment')
        }), )

admin.site.register(Notification, NotificationAdmin)