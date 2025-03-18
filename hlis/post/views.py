from io import BytesIO

from django.db import models
from django.db.models import Count, F
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from unicef_restlib.pagination import DynamicPageNumberPagination

from hlis.post.models import Post, Comments
from hlis.post.serializers import PostSerializer, PostFileSerializer, CommentsSerializer, LikeSerializers
import boto3


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DynamicPageNumberPagination

    @action(methods=['post'], detail=True, url_path='files', url_name='files')
    def set_product_photo(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = PostFileSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        data.update({'post': post})
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DynamicPageNumberPagination

    # def get_paginated_response(self, data):
    #     response = super().get_paginated_response(data)
    #     response.data.update(
    #         self.filter_queryset(self.get_queryset())
    #             .aggregate(total_commant=Count(F('id'), output_field=models.IntegerField()))
    #     )
    #     return response


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = LikeSerializers
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DynamicPageNumberPagination
