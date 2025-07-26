from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.static import serve
import os

urlpatterns = [
    path("admin/", admin.site.urls),
    path('<str:filename>.html', views.render_html),
    path('css/<path:path>', serve, {'document_root': os.path.join(settings.BASE_DIR, 'apps/static/css')}),
    path('js/<path:path>', serve, {'document_root': os.path.join(settings.BASE_DIR, 'apps/static/js')}),
    path('images/<path:path>', serve, {'document_root': os.path.join(settings.BASE_DIR, 'apps/static/images')}),
    path('users/', include('apps.users.urls')),
    path('products/', include('apps.products.urls')),
    path('', views.redirect_to_home)

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
