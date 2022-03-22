from rest_framework import serializers

from .models import Blog, Post

from accounts.serializers import UserSerializer

class BlogMinSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['title', 'description']
        model = Blog

class BlogSerializer(BlogMinSerializer):
    created_by = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Blog

    def get_created_by(self, instance):
        return UserSerializer(instance.created_by).data


class PostMinSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['title', 'content', 'published']
        model = Post

class PostSerializer(PostMinSerializer):
    created_by = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Post
    
    def get_created_by(self, instance):
        return UserSerializer(instance.created_by).data
