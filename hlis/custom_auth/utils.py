from django.utils import timezone


def forgot_password_expiration_time():
    return timezone.now() + timezone.timedelta(days=1)
