from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.conf import settings
import os
from .models import User
from .users_serializers import UserSerializer, UserUpdateSerializer, RegisterSerializer, LoginSerializer, ChangePasswordSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user

class AvatarUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'avatar' not in request.FILES:
            return Response({'error': '没有上传头像文件'}, status=status.HTTP_400_BAD_REQUEST)
        
        avatar_file = request.FILES['avatar']
        
        if avatar_file.size > 5 * 1024 * 1024:
            return Response({'error': '头像文件大小不能超过 5MB'}, status=status.HTTP_400_BAD_REQUEST)
        
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
        if avatar_file.content_type not in allowed_types:
            return Response({'error': '只支持 JPG、PNG、GIF 格式的图片'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        file_ext = avatar_file.name.split('.')[-1]
        file_name = f"avatar_{user.id}_{user.username}.{file_ext}"
        
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        file_path = os.path.join(upload_dir, file_name)
        
        if user.avatar and not user.avatar.startswith('http'):
            old_avatar_path = os.path.join(settings.MEDIA_ROOT, user.avatar.replace(settings.MEDIA_URL, ''))
            if os.path.exists(old_avatar_path):
                try:
                    os.remove(old_avatar_path)
                except:
                    pass
        
        with open(file_path, 'wb+') as destination:
            for chunk in avatar_file.chunks():
                destination.write(chunk)
        
        avatar_url = f"{settings.MEDIA_URL}avatars/{file_name}"
        user.avatar = avatar_url
        user.save(update_fields=['avatar'])
        
        return Response({
            'message': '头像上传成功',
            'avatar': avatar_url,
            'user': UserSerializer(user).data
        })

class TeacherListView(generics.ListAPIView):
    queryset = User.objects.filter(role='teacher')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class StudentListView(generics.ListAPIView):
    queryset = User.objects.filter(role='student')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChangePasswordView(APIView):
    """修改密码视图 - 增加了安全强度校验"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            new_password = serializer.validated_data['new_password']
            
            # 1. 验证旧密码
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'error': '旧密码不正确'}, status=status.HTTP_400_BAD_REQUEST)
            
            # 2. 核心修复：手动触发 Django 密码强度验证
            try:
                validate_password(new_password, user)
            except ValidationError as e:
                return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)
            
            # 3. 设置并保存新密码
            user.set_password(new_password)
            user.save()
            
            return Response({'message': '密码修改成功'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)