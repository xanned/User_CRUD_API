from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter

from api_token import views
from user.views import UserViewSet
from user_api import settings

schema_view = get_schema_view(
    openapi.Info(
        title="EXAMPLE API",
        default_version='v1',
        description="REST API Documentation",
        contact=openapi.Contact(email="example@example.com"),
    ),
    public=True,
)

router = SimpleRouter()
router.register(r'user', UserViewSet, basename='user')
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api-auth/', include('rest_framework.urls')),
                  path('api/', include(router.urls)),
                  re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                          name='schema-json'),
                  re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                  path('api-token-auth/', views.CustomAuthToken.as_view())
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
