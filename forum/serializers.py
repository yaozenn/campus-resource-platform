from rest_framework import serializers
from .models import ForumPost, ForumComment
from users.users_serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = ForumPost
        fields = ['id', 'title', 'author', 'content', 'post_date', 'status', 'visible_to', 'views', 'replies']

    def get_replies(self, obj):
        return obj.comments.count()

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumPost
        fields = ['title', 'content', 'visible_to']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ForumComment
        fields = ['id', 'author', 'post', 'content', 'comment_date']
