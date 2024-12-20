from django.contrib import admin
from .models import Notification

@admin.action(description="Mark selected as unread")
def mark_as_unread(modelAdmin, request, queryset):
    queryset.update(isRead = False)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at', 'isRead']
    ordering = ['-created_at']
    actions = [mark_as_unread]

# Register your models here.
admin.site.register(Notification,NotificationAdmin)