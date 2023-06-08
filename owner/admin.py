from django.contrib import admin
from .models import Owner
# Register your models here.
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['id','firstname', 'lastname', 'phone', 'email', 'id_card']
    list_filter = ['firstname', 'lastname']
admin.site.register(Owner, OwnerAdmin)