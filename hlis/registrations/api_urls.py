from django.urls import path, include

from rest_framework.routers import SimpleRouter

from hlis.registrations.views import RegistrationViewSet

router = SimpleRouter()

router.register('', RegistrationViewSet, basename='registration')


app_name = 'registration'

urlpatterns = [
    path('', include(router.urls)),
]