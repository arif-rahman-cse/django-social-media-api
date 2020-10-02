from rest_framework import routers
from django.urls import path, include
from .views import AuthViewSet

router = routers.DefaultRouter()
router.register('', AuthViewSet, basename='account')

urlpatterns = [
    path('reset-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
urlpatterns += router.urls
