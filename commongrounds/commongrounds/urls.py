"""
URL configuration for commongrounds project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path
from .views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    path('localevents/', include('localevents.urls', namespace="localevents")),
    path('commissions/', include('commissions.urls', namespace='commissions')),
    path('diyprojects/', include('diyprojects.urls', namespace='diyprojects')),
    path('merchstore/', include('merchstore.urls', namespace='merchstore')),
    path('bookclub/', include('bookclub.urls', namespace='bookclub')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
