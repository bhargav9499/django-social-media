import phonenumbers
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, Serializer

from hlis.custom_auth.models import ApplicationUser


class RegistrationSerializer(ModelSerializer):
    phone = PhoneNumberField(write_only=True)

    class Meta:
        model = ApplicationUser
        fields = ('first_name', 'last_name', 'username', 'country', 'email', 'phone', 'password',)
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True},
            'country': {'required': True},
            'email': {'required': True},
            'password': {'write_only': True, 'validators': [validate_password]},
        }
        read_only_fields = ('uuid',)

    def validate(self, attrs):
        try:
            phone = ApplicationUser.objects.filter(phone=attrs['phone'])
            print(attrs['phone'])
            if phone:
                raise ValidationError("Phone already exists!!")
            return super().validate(attrs)
        except KeyError:
            return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)

        # Convert Password into hash form
        user.set_password(password)
        user.save(update_fields=['password'])

        return user


class CheckUserDataSerializer(ModelSerializer):
    phone = PhoneNumberField()
    country_code = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()

    class Meta:
        model = ApplicationUser
        fields = ('first_name', 'last_name', 'username', 'country', 'email', 'phone', 'password', 'country_code',
                  'phone_number')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True},
            'country': {'required': True},
            'email': {'required': True},
            'password': {'validators': [validate_password]},
        }

    def validate(self, attrs):
        try:
            phone = ApplicationUser.objects.filter(phone=attrs['phone'])
            print(attrs['phone'])
            if phone:
                raise ValidationError("Phone already exists!!")
            return super().validate(attrs)
        except KeyError:
            return super().validate(attrs)


    def get_country_code(self, obj):
        try:
            phone = phonenumbers.parse(str(obj['phone']))
            return f'+{phone.country_code}'
        except phonenumbers.NumberParseException:
            return None

    def get_phone_number(self, obj):
        try:
            phone = phonenumbers.parse(str(obj['phone']))
            return f'+{phone.national_number}'
        except phonenumbers.NumberParseException:
            return None


class SendSmsCodeSerializer(Serializer):
    phone = PhoneNumberField(required=True)


class OTPVerification(Serializer):
    phone = PhoneNumberField(required=True)
    otp = serializers.CharField(max_length=4, required=True)
