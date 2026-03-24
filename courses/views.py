from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Resource, ResourceComment, ResourceCollection, ResourceType
from .serializers import ResourceSerializer, ResourceCreateSerializer, CommentSerializer, CollectionSerializer, CollectionCreateSerializer, ResourceTypeSerializer
from users.models import User


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


class TeacherResourceListView(generics.ListAPIView):
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resource.objects.filter(uploader=self.request.user)


class ResourceDetailView(generics.RetrieveAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.AllowAny]


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


class ResourceApproveView(generics.UpdateAPIView):
    queryset = Resource.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        resource = self.get_object()
        action = request.data.get('action')

        if action == 'approve':
            resource.status = 'active'
        elif action == 'reject':
            resource.status = 'rejected'
            resource.reject_reason = request.data.get('reason', '')

        resource.save()
        return Response(ResourceSerializer(resource).data)


class PendingResourceListView(generics.ListAPIView):
    queryset = Resource.objects.filter(status='pending')
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResourceCommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        resource_id = self.kwargs['pk']
        return ResourceComment.objects.filter(resource_id=resource_id)

    def perform_create(self, serializer):
        resource_id = self.kwargs['pk']
        serializer.save(user=self.request.user, resource_id=resource_id)


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


class ResourceCollectView(generics.CreateAPIView):
    serializer_class = CollectionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        resource_id = request.data.get('resource')
        user = request.user

        if ResourceCollection.objects.filter(user=user, resource_id=resource_id).exists():
            return Response({'error': '已经收藏过了'}, status=400)

        collection = ResourceCollection.objects.create(user=user, resource_id=resource_id)
        return Response(CollectionSerializer(collection).data)


class ResourceUncollectView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ResourceCollection.objects.filter(user=self.request.user)


class CollectionListView(generics.ListAPIView):
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ResourceCollection.objects.filter(user=self.request.user)


class ResourceDownloadView(generics.GenericAPIView):
    queryset = Resource.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        resource = self.get_object()

        if resource.status != 'active':
            return Response({'error': '资源未通过审核'}, status=400)

        resource.downloads += 1
        resource.save()

        return Response({'message': '下载成功'})


class CommentListView(generics.ListAPIView):
    queryset = ResourceComment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]