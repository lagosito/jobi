"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include, static
from django.contrib import admin

urlpatterns = [
    url(r'^verwalter/', admin.site.urls),
    url(r'^jobs/', include('data.urls', namespace='data')),
    url(r'^', include('user_custom.urls', namespace='user_c')),
    url(r'^se/', include('search.urls', namespace='search')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^newsletter/', include('newsletter.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),

]

# Adds MEDIA_URL and STATIC_URL config as defined in settings
urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'Jobi Administration Panel'
admin.site.site_title = 'Jobi Site Admin'
