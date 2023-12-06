from django.contrib import admin
from django.urls import path, include

import posts.urls
import users.urls

urlpatterns = [
    path('', include(posts.urls, namespace='Posts')),
    path('admin/', admin.site.urls),
    path('auth/', include(users.urls, namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
]
