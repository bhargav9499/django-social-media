from django.urls import path, include
from rest_framework import routers
from hlis.category import views

router = routers.SimpleRouter()
router.register('', views.CategoryViewSet, basename='category')

app_name = 'category'

urlpatterns = [
    path('', include(router.urls)),
]