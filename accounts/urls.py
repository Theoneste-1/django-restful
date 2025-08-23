import django.urls
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from accounts.views import AuthViewSet


router = DefaultRouter()
router.register('auth', AuthViewSet, basename='auth')

urlpatterns = [
    path("", include(router.urls)),
]