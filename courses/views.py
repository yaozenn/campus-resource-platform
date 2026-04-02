from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db import models
from .models import Resource, ResourceComment, ResourceCollection, ResourceType, ResourceReport
from .serializers import (
    ResourceSerializer, ResourceCreateSerializer, CommentSerializer, 
    CollectionSerializer, CollectionCreateSerializer, ResourceTypeSerializer, ReportSerializer
)

# --- 资源类型相关视图 ---
class ResourceTypeListView(generics.ListAPIView):
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeSerializer
    permission_classes = [permissions.AllowAny]

class ResourceTypeManageView(generics.ListCreateAPIView):
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class ResourceTypeDeleteView(generics.DestroyAPIView):
    queryset = ResourceType.objects.all()
    permission_classes = [permissions.IsAuthenticated]

# --- 资源核心业务视图 ---
class ResourceListView(generics.ListAPIView):
    serializer_class = ResourceSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Resource.objects.filter(status='active')
        resource_type = self.request.query_params.get('type')
        if resource_type:
            queryset = queryset.filter(type_id=resource_type)
        return queryset

class ResourceCreateView(generics.CreateAPIView):
    serializer_class = ResourceCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user, status='pending')

class ResourceDetailView(generics.RetrieveAPIView):
    """资源详情视图 - 增加了下载量自动统计逻辑"""
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # 核心修复：点击/获取资源详情时，下载次数原子性 +1
        Resource.objects.filter(pk=instance.pk).update(downloads=models.F('downloads') + 1)
        
        # 刷新实例以获取最新的下载数值返回给前端
        instance.refresh_from_db()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ResourceUpdateView(generics.UpdateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resource.objects.filter(uploader=self.request.user)

class ResourceDeleteView(generics.DestroyAPIView):
    queryset = Resource.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Resource.objects.all()
        return Resource.objects.filter(uploader=self.request.user)

# --- 审核与奖励逻辑 ---
class ResourceApproveView(generics.UpdateAPIView):
    queryset = Resource.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response({'error': '仅管理员可审核'}, status=403)
            
        resource = self.get_object()
        action = request.data.get('action')

        if action == 'approve':
            # 允许从“待审核”或“已拒绝”状态重新转为“已发布”
            if resource.status in ['pending', 'rejected']:
                resource.status = 'active'
                resource.reject_reason = "" # 审核通过时清空之前的拒绝原因
                
                # 资源审核通过奖励：20分
                uploader = resource.uploader
                if uploader.role == 'student':
                    uploader.add_points(20, 'upload', f"分享资源《{resource.title}》奖励")
            
        elif action == 'reject':
            resource.status = 'rejected'
            resource.reject_reason = request.data.get('reason', '')

        resource.save()
        return Response(ResourceSerializer(resource).data)

class PendingResourceListView(generics.ListAPIView):
    queryset = Resource.objects.filter(status='pending')
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]

# --- 评论与评分计算逻辑 ---
class ResourceCommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ResourceComment.objects.filter(resource_id=self.kwargs['pk'])

    def perform_create(self, serializer):
        user = self.request.user
        resource_id = self.kwargs['pk']
        
        # 1. 检查是否是首次评论该资源，防止无限刷分
        is_first_comment = not ResourceComment.objects.filter(user=user, resource_id=resource_id).exists()
        
        # 2. 保存评论（包含用户打分 user_rating）
        comment = serializer.save(user=user, resource_id=resource_id)
        
        # 3. 积分奖励：仅限学生且是首次评论奖励 10 分
        if user.role == 'student' and is_first_comment:
            user.add_points(10, 'post', f"参与资源《{comment.resource.title}》讨论")
            
        # 4. 直接调用模型方法更新评分数据
        comment.resource.update_rating()

class ResourceReportView(generics.CreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

class CollectionListView(generics.ListAPIView):
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return ResourceCollection.objects.filter(user=self.request.user)

class TeacherResourceListView(generics.ListAPIView):
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Resource.objects.filter(uploader=self.request.user)

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def comment_reply(request, pk):
    comment_id = request.data.get('comment_id')
    reply = request.data.get('reply', '')
    try:
        comment = ResourceComment.objects.get(id=comment_id, resource_id=pk)
        if comment.resource.uploader != request.user:
            return Response({'error': '无权限'}, status=403)
        comment.reply = reply
        comment.save()
        return Response(CommentSerializer(comment).data)
    except ResourceComment.DoesNotExist:
        return Response({'error': '评论不存在'}, status=404)