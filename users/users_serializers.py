from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    resource_count = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    collection_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'name', 'email', 'student_id', 'employee_id',
                  'gender', 'phone', 'signature', 'major', 'grade', 'subject', 'department',
                  'points', 'supervisor', 'avatar', 'resource_count', 'post_count', 'collection_count']

    def get_resource_count(self, obj):
        return obj.uploaded_resources.filter(status__in=['approved', 'active']).count()

    def get_post_count(self, obj):
        return obj.posts.filter(status='approved').count()

    def get_collection_count(self, obj):
        return obj.collections.count()


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['gender', 'phone', 'signature', 'major', 'grade', 'subject',
                  'department', 'name', 'email', 'student_id', 'employee_id', 'points']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'name', 'email', 'student_id', 'employee_id',
                  'gender', 'phone', 'signature', 'major', 'grade', 'subject', 'department']

    def create(self, validated_data):
        # 处理邮箱：如果为空或已存在，生成唯一邮箱
        email = validated_data.get('email', '').strip()
        if not email:
            email = f"{validated_data['username']}@example.com"
        else:
            # 检查邮箱是否已被使用
            if User.objects.filter(email=email).exists():
                email = f"{validated_data['username']}_{email.replace('@', '_at_')}"
        
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role', 'student'),
            name=validated_data.get('name', ''),
            email=email,
            student_id=validated_data.get('student_id', ''),
            employee_id=validated_data.get('employee_id', ''),
            gender=validated_data.get('gender', ''),
            phone=validated_data.get('phone', ''),
            signature=validated_data.get('signature', ''),
            major=validated_data.get('major', ''),
            grade=validated_data.get('grade', ''),
            subject=validated_data.get('subject', ''),
            department=validated_data.get('department', '')
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(required=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('用户名或密码错误，请检查您的输入')

        if user.role != data['role']:
            raise serializers.ValidationError(f'账号角色不正确，请使用{data["role"]}账号登录')
        
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=6)
    
    def validate_new_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('新密码长度不能少于 6 位')
        return value