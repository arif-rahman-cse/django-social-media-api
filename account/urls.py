from rest_framework import routers
from django.urls import path, include
from .views import AuthViewSet, UpdateProfileView

router = routers.DefaultRouter()
# router.register('my-profile/', ProfileViewSet, basename='profile')
router.register('', AuthViewSet, basename='account')

urlpatterns = [
    path('my-profile/', UpdateProfileView.as_view(), name='my-profile'),
    path('reset-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
urlpatterns += router.urls
