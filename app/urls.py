from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(), name="swagger-ui"),
    path("admin/", admin.site.urls),
    path("api/user/", include("user.urls"), name="User"),
    path("api/core/", include("core.urls"), name="Core"),
]
