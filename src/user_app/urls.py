"""user_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from user_app.views import HealthCheckAPI

admin.site.site_header = 'User Service API V1 Admin'  # default: "Django Administration"
admin.site.index_title = 'User Service API V1 Administration'  # default: "Site administration"
admin.site.site_title = 'User Service API V1 Admin'  # default: "Django site admin"

schema_view = get_schema_view(
   openapi.Info(
      title="Voting API",
      default_version='v1',
      description="API DOC of User Service API V1",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

v1_patterns = [
    path('', HealthCheckAPI.as_view(), name='health-check-api'),
    path('/users/', include('users.urls', namespace='users-api')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api', include([
            path('/v1', include(v1_patterns)),
    ])),

    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
