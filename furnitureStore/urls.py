from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
] + debug_toolbar_urls()

handler404 = views.page_not_found