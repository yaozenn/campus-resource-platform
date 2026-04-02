from rest_framework import serializers
from .models import Resource, ResourceType, ResourceComment, ResourceCollection, ResourceReport
from users.users_serializers import UserSerializer

class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='type.name', read_only=True)
    uploader_info = UserSerializer(source='uploader', read_only=True)

    class Meta:
        model = Resource
        fields = '__all__'

class ResourceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        exclude = ('uploader', 'status', 'reject_reason', 'downloads', 'rating', 'rating_count')

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.URLField(source='user.avatar', read_only=True)

    class Meta:
        model = ResourceComment
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceReport
        fields = ('resource', 'reason', 'description')

class CollectionSerializer(serializers.ModelSerializer):
    resource_details = ResourceSerializer(source='resource', read_only=True)
    class Meta:
        model = ResourceCollection
        fields = '__all__'

class CollectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceCollection
        fields = ('resource',)