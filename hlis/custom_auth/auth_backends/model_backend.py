from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.utils.translation import ugettext as _

from rest_framework.exceptions import PermissionDenied


class CustomModelBackends(ModelBackend):
    """
    Authentication user using email or username
    """

    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        if not username and not email:
            return None

        UserModel = get_user_model()

        username_query_dict = {'username__iexact': username}
        email_query_dict = {'email__iexact': email}

        try:
            query_filter = Q()
            if username:
                query_filter |= Q(**username_query_dict)

            if email:
                query_filter |= Q(**email_query_dict)

            user = UserModel.objects.get(query_filter)
            if not user.is_active:
                return PermissionDenied(_('User is not Active'))

        except UserModel.DoesNotExist:
            return None

        else:
            if user.check_password(password):
                return user

        return None
