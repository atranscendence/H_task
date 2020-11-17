from django.contrib import admin
from main_app import models
from simple_history.admin import SimpleHistoryAdmin
from simple_history import register
from django.contrib.auth.models import User

register(User)
admin.site.register(models.Documents, SimpleHistoryAdmin)


@admin.register(models.AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ['action', 'username', 'ip', ]
    list_filter = ['action', ]
