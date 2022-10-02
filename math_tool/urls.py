from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import RenderViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"math/?", RenderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
