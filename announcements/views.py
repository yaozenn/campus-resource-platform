from rest_framework import generics, permissions
from .models import Announcement
from .serializers import AnnouncementSerializer, AnnouncementCreateSerializer

class AnnouncementListView(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Announcement.objects.filter(status='active')
        user_role = self.request.query_params.get('role')
        
        if user_role:
            queryset = queryset.filter(visible_to__in=['all', user_role])
        else:
            queryset = queryset.filter(visible_to='all')
        
        return queryset

class AnnouncementCreateView(generics.CreateAPIView):
    serializer_class = AnnouncementCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class AnnouncementDetailView(generics.RetrieveAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.AllowAny]

class AnnouncementUpdateView(generics.UpdateAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Announcement.objects.filter(author=self.request.user)

class AnnouncementDeleteView(generics.DestroyAPIView):
    queryset = Announcement.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Announcement.objects.filter(author=self.request.user)
