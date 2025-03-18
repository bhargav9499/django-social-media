from django.urls import path, include
from rest_framework import routers
from hlis.custom_auth import views

router = routers.SimpleRouter()
router.register('auth', views.UserAuthViewSet, basename='auth')
router.register('users', views.UserViewSet, basename='users')

app_name = 'custom_auth'

urlpatterns = [
    path('', include(router.urls)),
]