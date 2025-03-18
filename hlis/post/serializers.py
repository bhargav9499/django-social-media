import os

from rest_framework import serializers, status
from rest_framework.response import Response

from hlis.category.serializers import CategorySerializer
from hlis.custom_auth.models import ApplicationUser
from hlis.custom_auth.serializers import BaseUserSerializer
from hlis.post.models import Post, PostFile, Tag, HashTag, Comments, Likes


class LikeSerializers(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = Likes
        fields = ("id", "user", "post", "like")
        extra_kwargs = {
            'like': {'required': True},
        }

    # def create(self, validated_data):
    #     like, created = Likes.objects.get_or_create(post=validated_data['post'], user=self.context['request'].user)
    #     if like:
    #         like.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     elif created:
    #         return Response(status=status.HTTP_201_CREATED)

    def create(self, validated_data):
        like = Likes.objects.filter(post=validated_data['post'], user=self.context['request'].user).first()
        if like:
            return super().update(like, validated_data)
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CommentsSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comments
        fields = ("id", "user", "user_id", "post", "comment")
        extra_kwargs = {
            'user_id': {'required': True},
            'comment': {'required': True},
        }

    def create(self, validated_data):
        validated_data["user"] = ApplicationUser.objects.get(id=validated_data['user_id'])
        return super().create(validated_data)


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ('id', 'user_hashtag',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'user_tag',)


class PostFileSerializer(serializers.ModelSerializer):
    post_file = serializers.FileField(required=True)

    class Meta:
        model = PostFile
        fields = ('id', 'post_file',)
        # extra_kwargs = {
        #     'post_file': {'required': True},
        # }

    # def validate(self, attrs):
    #     validated_data = super().validate(attrs)
    #     MAX_VIDEO_SIZE = 63 * 1024 * 1024  # 50MB in bytes
    #     print("MAX_VIDEO_SIZE", MAX_VIDEO_SIZE)
    #     print("post_file : ", attrs['post_file'].size)
    #     if attrs['post_file'].size > MAX_VIDEO_SIZE:
    #         raise serializers.ValidationError("Video size should not exceed 50MB.")
    #     return validated_data

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        video = attrs['post_file']
        extension = os.path.splitext(video.name)[1]
        # print(extension)
        if video is not None and extension in ['.mp4', '.avi', '.mov']:
            MAX_VIDEO_SIZE = 63 * 1024 * 1024  # 50MB in bytes
            # print("MAX_VIDEO_SIZE", MAX_VIDEO_SIZE)
            # print("post_file : ", attrs['post_file'].size)
            if attrs['post_file'].size > MAX_VIDEO_SIZE:
                raise serializers.ValidationError("Video size should not exceed 50MB.")
        return validated_data

class PostSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)
    category_details = CategorySerializer(source='category', read_only=True)
    post_file = PostFileSerializer(read_only=True, many=True)
    post_tag = TagSerializer(read_only=True, many=True)
    post_hashtag = HashTagSerializer(read_only=True, many=True)
    tag = serializers.ListField(child=serializers.CharField(), required=True, max_length=255, write_only=True)
    hashtag = serializers.ListField(child=serializers.CharField(), required=True, max_length=255, write_only=True)
    comment_details = CommentsSerializer(read_only=True, many=True)
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'category_details', 'caption', 'title', 'post_file', 'post_tag',
                  'post_hashtag', 'tag', 'hashtag', 'comment_details', 'comment_count', 'like_count')
        extra_kwargs = {
            'caption': {'required': True},
            'title': {'required': True},
            'category': {'required': True},
        }

    def get_comment_count(self, obj):
        return Comments.objects.filter(post=obj).count()

    def get_like_count(self, obj):
        return Likes.objects.filter(post=obj, like=1).count()

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        tag = validated_data.pop('tag')
        hashtag = validated_data.pop('hashtag')
        data = super().create(validated_data)
        Tag.objects.create(post=data, user_tag=tag)
        HashTag.objects.create(post=data, user_hashtag=hashtag)

        return data


