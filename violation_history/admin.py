from django.contrib import admin
from .models import ViolationHistory, UnsureViolationHistory, Violation
# Register your models here.
class ViolationHistoryAdmin(admin.ModelAdmin):
    # list_display = ['id','description', 'time','status', 'fee', 'vehicle']
    list_display = ['id', 'time','status', 'vehicle']
    list_filter = ['vehicle']

class UnsureViolationAdmin(admin.ModelAdmin):
    list_display = ['id','description', 'time']

class ViolationAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'fee']

admin.site.register(ViolationHistory, ViolationHistoryAdmin)
admin.site.register(UnsureViolationHistory, UnsureViolationAdmin)
admin.site.register(Violation, ViolationAdmin)