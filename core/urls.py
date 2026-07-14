from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('api/users/', include('users.urls')),
    path('api/organizations/', include('organization.urls')),
    path('api/memberships/', include('membership.urls')),
    path('api/news/', include('news.urls')),
    path('api/petitions/', include('petitions.urls')),
]
