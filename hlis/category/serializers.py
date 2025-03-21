from rest_framework import serializers
from hlis.category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug',)
        read_only_fields = ('slug',)

