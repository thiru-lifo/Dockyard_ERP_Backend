from django.contrib import admin
from master.models import Countries, States

class CountriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'phone_code', 'currency', 'status')
    list_filter = ("name", "code", "phone_code")
    search_fields = ("name", "code", "phone_code")
    #readonly_fields = ('created_on', 'modified_on',)
    

    fieldsets = (
        ('Standard info', {
            'fields': ('name', 'code', 'phone_code', 'currency','status' )
        }), )

    def save_model(self, request, obj, form, change):
        if not change:
            
            obj.created_by = 1
            obj.created_ip = request.META.get('REMOTE_ADDR')
        else:
            
            obj.modified_by = 1
            obj.modified_ip = request.META.get('REMOTE_ADDR')

        obj.save()



class StatesAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status')
    list_filter = ("name", "code")
    search_fields = ("name", "code")
    #readonly_fields = ('created_on', 'modified_on',)
    
    fieldsets = (
        ('Standard info', {
            'fields': ('name', 'code', 'country_id', 'status' )
        }), )

    def save_model(self, request, obj, form, change):
        if not change:
            
            obj.created_by = 1
            obj.created_ip = request.META.get('REMOTE_ADDR')
        else:
            
            obj.modified_by = 1
            obj.modified_ip = request.META.get('REMOTE_ADDR')

        obj.save()



    
admin.site.register(Countries, CountriesAdmin)
admin.site.register(States, StatesAdmin)