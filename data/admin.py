from django.contrib import admin

from data.models import Source


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'verbose_name', 'ds_type', 'call_method', 'es_structure', 'ex_details', 'refresh_rate',
                    'counter', 'error_count', 'scrapper_active', 'last_finished_at', 'update_time', 'create_time')


admin.site.register(Source, SourceAdmin)
