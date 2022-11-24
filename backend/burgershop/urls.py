from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

from django.conf import settings

from .apps.main.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='start_page'),
    path('api/', include('burgershop.apps.urls')),
    path('manager/', include('burgershop.apps.restaurateur.urls')),
    path('api-auth/', include('rest_framework.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
