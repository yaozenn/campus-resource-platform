from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import ForumPost, ForumComment
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer

class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = ForumPost.objects.filter(status='approved')
        user_role = self.request.query_params.get('role')
        if user_role:
            queryset = queryset.filter(visible_to__in=['all', user_role])
        else:
            queryset = queryset.filter(visible_to='all')
        return queryset

class PostCreateView(generics.CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        # 修复低级失误：论坛发帖奖励修改为 20 分！
        user = self.request.user
        if user.role == 'student':
            user.add_points(20, 'post', f"发布论坛帖子《{post.title[:15]}》")

class PostDetailView(generics.RetrieveAPIView):
    queryset = ForumPost.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

class PostViewCountView(generics.GenericAPIView):
    queryset = ForumPost.objects.all()
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        post.views = (post.views or 0) + 1
        post.save(update_fields=['views'])
        return Response({'status': 'ok', 'views': post.views})

class PostUpdateView(generics.UpdateAPIView):
    queryset = ForumPost.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ForumPost.objects.filter(author=self.request.user)

class PostDeleteView(generics.DestroyAPIView):
    queryset = ForumPost.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 作者本人或管理员可以删除
        if self.request.user.role == 'admin':
            return ForumPost.objects.all()
        return ForumPost.objects.filter(author=self.request.user)

class PostCommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return ForumComment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        # 参与论坛讨论（回复）奖励：10 分
        user = self.request.user
        comment = serializer.save(author=user, post_id=self.kwargs['pk'])
        if user.role == 'student':
            user.add_points(10, 'post', f"参与帖子《{comment.post.title[:15]}》讨论")

class CommentListView(generics.ListAPIView):
    queryset = ForumComment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]