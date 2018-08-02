from rest_framework import serializers
from .models import Post, Author, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Tag

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Author

class PostHtmlSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        exclude = ('html', )