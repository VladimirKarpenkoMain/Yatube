from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import posts.urls
import users.urls
import about.urls

urlpatterns = [
    path('', include(posts.urls, namespace='Posts')),
    path('admin/', admin.site.urls),
    path('about/', include(about.urls, namespace='about')),
    path('auth/', include(users.urls, namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
]

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
handler403 = 'core.views.permission_denied_view'

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )