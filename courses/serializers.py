from rest_framework import serializers
from .models import Resource, ResourceType, ResourceComment, ResourceCollection, ResourceReport
from users.users_serializers import UserSerializer

class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='type.name', read_only=True)
    type_description = serializers.CharField(source='type.description', read_only=True)
    uploader_info = UserSerializer(source='uploader', read_only=True)
    uploader_name = serializers.CharField(source='uploader.name', read_only=True, allow_null=True)
    uploader_username = serializers.CharField(source='uploader.username', read_only=True, allow_null=True)

    class Meta:
        model = Resource
        fields = '__all__'

class ResourceCreateSerializer(serializers.ModelSerializer):
    type_id = serializers.IntegerField(
        required=True,
        error_messages={'required': '请选择资源分类', 'does_not_exist': '所选分类不存在'}
    )
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    is_second_hand = serializers.BooleanField(required=False, default=False)
    points_required = serializers.IntegerField(required=False, default=0)
    
    class Meta:
        model = Resource
        exclude = ('uploader', 'status', 'reject_reason', 'downloads', 'rating', 'rating_count', 'type')

    def validate_type_id(self, value):
        try:
            ResourceType.objects.get(id=value)
        except ResourceType.DoesNotExist:
            raise serializers.ValidationError('所选分类不存在')
        return value
    
    def validate_file_url(self, value):
        if value and not value.startswith(('http://', 'https://')):
            return 'http://' + value
        return value
    
    def create(self, validated_data):
        type_id = validated_data.pop('type_id')
        resource_type = ResourceType.objects.get(id=type_id)
        validated_data['type'] = resource_type
        return Resource.objects.create(**validated_data)

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.URLField(source='user.avatar', read_only=True)
    created_at = serializers.DateTimeField(source='comment_date', read_only=True)

    class Meta:
        model = ResourceComment
        fields = '__all__'
        read_only_fields = ('user', 'resource', 'comment_date', 'reply')

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