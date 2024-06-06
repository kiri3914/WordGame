
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from authorization.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authorization.urls')),
    path('', home, name='home'),
    path('wordgame/', include('wordgame.urls')),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)