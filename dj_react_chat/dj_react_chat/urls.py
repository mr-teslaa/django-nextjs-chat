# dj_react_chat\dj_react_chat\urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from server.views import ServerListViewSet

router = DefaultRouter()
router.register("api/v1/server/select", ServerListViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    # API Documentation
    path("api/docs/schema", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/schema/ui",
        SpectacularSwaggerView.as_view(),
    ),
] + router.urls

# SERVE THE IMAGES FROM MEDIA FOLDER
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
