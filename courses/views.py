# 建议直接覆盖 courses/views.py
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
        # 管理员可以看到所有资源
        if hasattr(self.request, 'user') and self.request.user.is_authenticated and self.request.user.role == 'admin':
            return Resource.objects.all()
        # 普通用户只看已发布的
        queryset = Resource.objects.filter(status='active')
        resource_type = self.request.query_params.get('type')
        if resource_type:
            queryset = queryset.filter(type_id=resource_type)
        return queryset

class ResourceCreateView(generics.CreateAPIView):
    serializer_class = ResourceCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print('接收到的请求数据:', request.data)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print('验证失败详情:', serializer.errors)
            return Response(serializer.errors, status=400)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user, status='pending')

class ResourceDetailView(generics.RetrieveAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.AllowAny]

# 新增：专门处理下载统计的视图
class ResourceDownloadView(generics.GenericAPIView):
    queryset = Resource.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        resource = self.get_object()
        # 原子性增加下载次数
        Resource.objects.filter(pk=resource.pk).update(downloads=models.F('downloads') + 1)
        return Response({'status': 'success', 'file_url': resource.file_url})

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
            resource.status = 'active'
            resource.reject_reason = ""
            uploader = resource.uploader
            if uploader.role == 'student':
                uploader.add_points(20, 'upload', f"分享资源《{resource.title}》奖励")
        elif action == 'reject':
            resource.status = 'rejected'
            resource.reject_reason = request.data.get('reason', '')

        resource.save()
        return Response(ResourceSerializer(resource).data)

class ResourceStatusUpdateView(generics.UpdateAPIView):
    queryset = Resource.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response({'detail': '仅管理员可操作'}, status=403)
            
        resource = self.get_object()
        status_value = request.data.get('status')
        
        if status_value not in ['active', 'pending', 'rejected']:
            return Response({'detail': '无效的状态值'}, status=400)
        
        if status_value == 'active' and resource.status != 'active':
            uploader = resource.uploader
            if uploader and uploader.role == 'student':
                try:
                    uploader.add_points(20, 'upload', f"分享资源《{resource.title}》奖励")
                except:
                    pass
        
        resource.status = status_value
        resource.save()
        return Response({'status': 'success', 'resource': ResourceSerializer(resource).data})

class PendingResourceListView(generics.ListAPIView):
    queryset = Resource.objects.filter(status='pending')
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]

# --- 收藏功能 ---
class CollectionListView(generics.ListAPIView):
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return ResourceCollection.objects.filter(user=self.request.user)

class CollectionCreateView(generics.CreateAPIView):
    serializer_class = CollectionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# 新增：取消收藏视图
class CollectionDeleteView(generics.DestroyAPIView):
    queryset = ResourceCollection.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return ResourceCollection.objects.filter(user=self.request.user)

# --- 评论与举报 ---
class ResourceCommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ResourceComment.objects.filter(resource_id=self.kwargs['pk'])

    def perform_create(self, serializer):
        user = self.request.user
        resource_id = self.kwargs['pk']
        is_first_comment = not ResourceComment.objects.filter(user=user, resource_id=resource_id).exists()
        comment = serializer.save(user=user, resource_id=resource_id)
        if user.role == 'student' and is_first_comment:
            user.add_points(10, 'post', f"参与资源《{comment.resource.title}》讨论")
        comment.resource.update_rating()

class ResourceReportView(generics.CreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        resource_id = self.kwargs['pk']
        resource = Resource.objects.get(pk=resource_id)
        serializer.save(reporter=self.request.user, resource=resource)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def resource_rate(request, pk):
    try:
        resource = Resource.objects.get(pk=pk)
        rating = request.data.get('rating')
        if not rating or not 1 <= rating <= 5:
            return Response({'error': '评分必须在1-5之间'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查用户是否已经评过分，如果有就更新，没有就创建一个评论
        user = request.user
        comment, created = ResourceComment.objects.get_or_create(
            user=user,
            resource=resource,
            defaults={'content': '用户评分', 'user_rating': rating}
        )
        
        if not created:
            comment.user_rating = rating
            comment.save()
        
        # 更新资源评分
        resource.update_rating()
        
        return Response({
            'success': True,
            'rating': resource.rating,
            'rating_count': resource.rating_count
        })
    except Resource.DoesNotExist:
        return Response({'error': '资源不存在'}, status=status.HTTP_404_NOT_FOUND)

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