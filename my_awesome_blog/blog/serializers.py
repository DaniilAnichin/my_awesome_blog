from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Post, Tag


User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)

    def run_validators(self, value):
        pass

    def to_representation(self, instance):
        return str(instance)

    def to_internal_value(self, data):
        return data


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        exclude = ()

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        instance = super().create(validated_data)
        instance.set_tags(tags)
        return instance

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        instance = super().update(instance, validated_data)
        instance.set_tags(tags)
        return instance


class AuthorSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'username', 'posts')
