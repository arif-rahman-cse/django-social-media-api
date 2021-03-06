from django.contrib.auth import get_user_model, logout, authenticate
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .utils import create_user_account
from .models import Profile

User = get_user_model()


class UpdateProfileView(APIView):
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        user_profile = Profile.objects.get(user=user)
        serializer = serializers.UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        user_profile = Profile.objects.get(user=user)
        serializer = serializers.UserProfileSerializer(data=request.data, instance=user_profile)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = serializers.EmptySerializer
    serializer_classes = {
        'login': serializers.UserLoginSerializer,
        'register': serializers.UserRegisterSerializer,
        'password_change': serializers.PasswordChangeSerializer,
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user is None:
            data = {
                "error": "Invalid username or password. Please try again with a valid username or password!"
            }
        else:
            data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        logout(request)
        data = {'success': 'You have been logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated, ], url_path='change-password')
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['new_password'] != serializer.validated_data['new_password_2']:
            data = {
                "error": "Please provide same password for both new password fields"
            }
            return Response(data=data, status=status.HTTP_406_NOT_ACCEPTABLE)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        data = {
            "success": "Password reset successful!"
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
