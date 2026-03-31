"""
URL configuration for commongrounds project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    path('localevents/', include('localevents.urls', namespace="localevents")),
    path('commissions/', include('commissions.urls')),
    path('diyprojects/', include('diyprojects.urls', namespace='diyprojects')),
    path('merchstore/', include('merchstore.urls', namespace='merchstore')),
    path('bookclub/', include('bookclub.urls', namespace='bookclub')),
]
