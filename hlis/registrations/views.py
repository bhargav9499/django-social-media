from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from unicef_restlib.views import MultiSerializerViewSetMixin

from hlis.custom_auth.models import ApplicationUser
from hlis.registrations.serializers import RegistrationSerializer, CheckUserDataSerializer, \
    SendSmsCodeSerializer, OTPVerification

otp = "9999"


class RegistrationViewSet(
    MultiSerializerViewSetMixin,
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = ApplicationUser.objects.all()
    serializer_class = RegistrationSerializer
    serializer_action_classes = {
        'check_user_data': CheckUserDataSerializer,
        'send_sms_code': SendSmsCodeSerializer,
        'otp_verification': OTPVerification,
    }
    permission_classes = (AllowAny,)

    @action(methods=['post'], permission_classes=(AllowAny,), url_name='check_user_data',
            url_path='check-user-data', detail=False)
    def check_user_data(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # send OTP first time when data is valid
        data = serializer.data
        data.update({'otp': otp})
        return Response(data)

    @action(permission_classes=(AllowAny,), methods=['post'], url_name='send_sms_code',
            url_path='send-sms-code', detail=False)
    def send_sms_code(self, *args, **kwargs):
        """
        Send Again OTP if they request
        """
        serializer = self.get_serializer(data=self.request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'otp': otp})

    @action(permission_classes=(AllowAny,), methods=['post'], url_name='otp_verification',
            url_path='otp-verification', detail=False)
    def otp_verification(self, *args, **kwargs, ):
        serializer = self.get_serializer(data=self.request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if otp != serializer.data['otp']:
            raise ValidationError("Please enter valid OTP")
        return Response("OTP Verified")
