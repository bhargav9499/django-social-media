from typing import Type

from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from unicef_restlib.pagination import DynamicPageNumberPagination

from hlis.custom_auth.models import ForgotPassword
from hlis.custom_auth.serializers import UserAuthSerializer, BaseUserSerializer, PasswordValidationSerializer

User = get_user_model()


class UserAuthViewSet(viewsets.ViewSet):

    def _auth(self, request, *args, **kwargs):
        auth_serializer = UserAuthSerializer(data=request.data, context={'request': request, 'view': self})
        auth_serializer.is_valid(raise_exception=True)

        user = authenticate(request, **auth_serializer.data)
        if not user:
            raise ValidationError('Invalid credentials')

        user_details = BaseUserSerializer(instance=user).data
        user_details.update({'X-Token': user.user_auth_tokens.create().key})

        return Response(data=user_details, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny],
            url_name='login', url_path='login')
    def login(self, request, *args, **kwargs):
        return self._auth(request, *args, **kwargs)

    @action(methods=['delete'], detail=False)
    def logout(self, request, *args, **kwargs):
        if request.user.user_auth_tokens.count() > 1:
            self.request.auth.delete()
        else:
            request.user.user_auth_tokens.all().delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'uuid'
    pagination_class = DynamicPageNumberPagination

    filter_backends = (DjangoFilterBackend, SearchFilter)

    def get_permissions(self):
        if self.action == 'password_reset_change_password':
            return [permissions.AllowAny()]

        return super().get_permissions()

    def _get_base_serializer_class(self):
        if self.action == 'list':
            return BaseUserSerializer

        if self.action == 'password_reset_change_password':
            return PasswordValidationSerializer

        return BaseUserSerializer

    def get_serializer_class(self) -> Type[BaseUserSerializer]:
        serializer_class = self._get_base_serializer_class()
        return serializer_class

    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny],
            url_path='forgot-password', url_name='forgot_password')
    def forgot_password_via_email(self, request, *args, **kwargs):
        user_model = User
        user_email = request.data.get('email')
        if not user_email:
            raise ValidationError(_("Email is required."))

        user = user_model.objects.filter(email__iexact=user_email).first()
        if not user:
            raise NotFound(_("User doesn't exists."))
        forget_password_obj = ForgotPassword.objects.create(user=user)
        return Response({'id': forget_password_obj.id})

    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny],
            url_path='reset-password/(?P<password_reset_id>.*)', url_name='reset_password')
    def password_reset_change_password(self, request, *args, **kwargs):
        password_reset_obj = get_object_or_404(
            ForgotPassword,
            pk=self.kwargs.get('password_reset_id'),
            expiration_time__gt=timezone.now()
        )

        serializer = self.get_serializer_class()(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(pk=password_reset_obj.user.id)

        user.set_password(serializer.data['password'])
        user.save()

        ForgotPassword.objects.filter(pk=password_reset_obj.pk).delete()

        return Response(_("Password reset successfully!"))