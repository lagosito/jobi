from django.contrib import admin

from admin_custom.models import ActivityLog


class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('actor', 'entity', 'level', 'meta_info', 'create_time')


admin.site.register(ActivityLog, ActivityLogAdmin)
