import uuid as uuid

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from model_utils import Choices
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from hlis.custom_auth.managers import ApplicationUserManager
from hlis.custom_auth.mixins import UserPhotoMixin
from hlis.custom_auth.utils import forgot_password_expiration_time


class ApplicationUser(
    AbstractBaseUser,
    PermissionsMixin,
    UserPhotoMixin,
):
    GENDER_TYPES = Choices(
        ("male", "Male"),
        ("female", "Female"),
    )

    username_validator = UnicodeUsernameValidator()
    uuid = models.UUIDField(
        verbose_name=_('uuid'),
        unique=True,
        help_text=_('Required. A 32 hexadecimal digits number as specified in RFC 4122'),
        error_messages={
            'unique': _('A user with that uuid already exists.'),
        },
        default=uuid.uuid4,
    )
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_('Required, 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    country = models.CharField(_('country'), max_length=50, null=True, blank=True)
    email = models.EmailField(_('email address'), null=True, blank=True, unique=True,
                              error_messages={'unique': _('A user with that email already exists.'), }, )
    phone = PhoneNumberField(_('Phone'), null=True, blank=True, unique=True)
    about = models.TextField(_('about me'), max_length=1200, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPES, default=GENDER_TYPES.male)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_modified = models.DateTimeField(_('last modified'), auto_now=True)
    last_user_activity = models.DateTimeField(_('last activity'), default=timezone.now)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = ApplicationUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username or self.email or self.first_name or self.last_name or str(self.uuid)

    def save(self, *args, **kwargs):
        if self.photo and (not self.width_photo or not self.height_photo):
            self.width_photo = self.photo.width
            self.height_photo = self.photo.height

        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email)

        return super(ApplicationUser, self).save(*args, **kwargs)

    def update_last_activity(self):
        now = timezone.now()

        self.last_user_activity = now
        self.save(update_fields=('last_user_activity', 'last_modified'))


class ForgotPassword(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expiration_time = models.DateTimeField(default=forgot_password_expiration_time)

    class Meta:
        verbose_name = 'Forgot Password Id'




