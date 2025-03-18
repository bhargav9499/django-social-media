from django.urls import path, include
from rest_framework import routers
from hlis.post import views

router = routers.SimpleRouter()
router.register('posts', views.PostViewSet, basename='post')
router.register('comments', views.CommentViewSet, basename='comments')
router.register('likes', views.LikeViewSet, basename='likes')

app_name = 'post'

urlpatterns = [
    path('', include(router.urls)),
]
