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
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveAPIView):
    queryset = ForumPost.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

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
        return ForumPost.objects.filter(author=self.request.user)

class PostCommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return ForumComment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(author=self.request.user, post_id=post_id)

class CommentListView(generics.ListAPIView):
    queryset = ForumComment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]
