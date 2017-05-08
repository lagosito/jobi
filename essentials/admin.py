# Register your models here.
from django.contrib import admin
from essentials.models import NewsletterSubscription


class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'keywords')


admin.site.register(NewsletterSubscription, NewsletterSubscriptionAdmin)