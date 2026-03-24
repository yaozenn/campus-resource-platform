from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'name', 'email', 'student_id', 'employee_id',
                  'gender', 'phone', 'signature', 'major', 'grade', 'subject', 'department', 'points']


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
        # 空邮箱转 None，避免唯一约束冲突
        email = validated_data.get('email') or None
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