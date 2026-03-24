from rest_framework import serializers
from .models import Announcement
from users.users_serializers import UserSerializer

class AnnouncementSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'author', 'publish_date', 'status', 'visible_to']

class AnnouncementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'visible_to']
