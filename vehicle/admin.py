from django.contrib import admin
from .models import Vehicle
# Register your models here.

class VehicleAdmin(admin.ModelAdmin):
    list_display = ['id','plate', 'title', 'color', 'owner']
    list_filter = ['owner']

admin.site.register(Vehicle, VehicleAdmin)