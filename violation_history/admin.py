from django.contrib import admin
from .models import ViolationHistory, UnsureViolationHistory
# Register your models here.
class ViolationHistoryAdmin(admin.ModelAdmin):
    list_display = ['id','description', 'time','status', 'fee', 'vehicle']
    list_filter = ['vehicle']

class UnsureViolationAdmin(admin.ModelAdmin):
    list_display = ['id','description', 'time']

admin.site.register(ViolationHistory, ViolationHistoryAdmin)
admin.site.register(UnsureViolationHistory, UnsureViolationAdmin)