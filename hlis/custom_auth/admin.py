from datetime import timedelta

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.db.models import Case, When, Value, BooleanField
from django.utils import timezone

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    # password change from admin side
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    # Fieldsets
    fieldsets = (
        ('Personal Details', {'fields': ('uuid', 'username', 'first_name', 'last_name', 'country', 'email',
                                         'phone', 'about', 'gender', 'password',)}),
        ('Statues', {'fields': ('is_active',)}),
        ('Service', {'fields': ('is_staff', 'is_superuser',)}),
        ('Account dates', {'fields': ('date_joined', 'last_user_activity', 'last_modified',)}),
    )
    readonly_fields = ('uuid', 'first_name', 'last_name', 'date_joined', 'last_user_activity', 'last_modified',)
    list_display = ('id', 'email', '_get_password', 'date_joined', 'uuid', 'is_online',)
    search_fields = ('email', 'uuid', 'phone')

    def _get_password(self, obj):
        return 'Yes' if obj.password not in [None, ''] else 'No'

    _get_password.short_description = 'PASSWORD'
    _get_password.admin_order_field = 'password'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            is_online=Case(
                When(last_user_activity__gte=timezone.now() - timedelta(minutes=10), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )

    def is_online(self, obj):
        return obj.is_online

    is_online.boolean = True
    is_online.admin_order_field = 'is_online'