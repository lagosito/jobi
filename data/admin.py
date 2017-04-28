from django.contrib import admin

from data.models import Source


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'verbose_name', 'ds_type', 'call_method', 'call_kwargs', 'ex_details', 'update_time',
                    'create_time')


admin.site.register(Source, SourceAdmin)
