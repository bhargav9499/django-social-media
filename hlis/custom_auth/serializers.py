import phonenumbers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class UserAuthSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    country_code = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()

    class Meta:
        model = User  # ApplicationUser
        fields = ('id', 'uuid', 'first_name', 'last_name', 'username', 'country', 'email', 'phone', 'password',
                  'country_code', 'phone_number',)
        read_only_fields = ('uuid',)

    def get_country_code(self, obj):
        try:
            phone = phonenumbers.parse(str(obj.phone))
            return f'+{phone.country_code}'
        except phonenumbers.NumberParseException:
            return None

    def get_phone_number(self, obj):
        try:
            phone = phonenumbers.parse(str(obj.phone))
            return str(phone.national_number)
        except phonenumbers.NumberParseException:
            return None

    def save(self, **kwargs):
        password = self.validated_data.pop('password', None)
        user = super().save(**kwargs)

        if password:
            user.set_password(password)
            user.save(update_fields=['password'])

        return user


class PasswordValidationSerializer(serializers.Serializer):
    password = serializers.CharField()

    def validate_password(self, password):
        try:
            validate_password(password)
        except DjangoValidationError as ex:
            raise ValidationError(ex.messages)
        return password
