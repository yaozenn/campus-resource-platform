from rest_framework import serializers
from .models import Resource, ResourceComment, ResourceCollection, ResourceType
from users.users_serializers import UserSerializer

class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    type_name = serializers.CharField(source='type.name', read_only=True)

    class Meta:
        model = Resource
        fields = ['id', 'title', 'type', 'type_name', 'teacher', 'description', 'file_url', 'upload_date', 'downloads', 'points_required', 'status', 'reject_reason', 'is_second_hand', 'price', 'cover_image']

class ResourceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['title', 'type', 'description', 'file_url', 'points_required', 'is_second_hand', 'price', 'cover_image']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    resource = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ResourceComment
        fields = ['id', 'user', 'resource', 'content', 'comment_date', 'reply']

class CollectionSerializer(serializers.ModelSerializer):
    resource = ResourceSerializer(read_only=True)

    class Meta:
        model = ResourceCollection
        fields = ['id', 'resource', 'collect_date']

class CollectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceCollection
        fields = ['resource']
