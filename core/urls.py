from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/organizations/', include('organization.urls')),
    path('api/memberships/', include('membership.urls')),
    path('api/news/', include('news.urls')),
    path('api/petitions/', include('petitions.urls')),
]
