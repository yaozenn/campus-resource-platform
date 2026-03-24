from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib.staticfiles.views import serve
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

BASE_DIR = settings.BASE_DIR

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/forum/', include('forum.urls')),
    path('api/announcements/', include('announcements.urls')),
    path('api/points/', include('points.urls')),
    path('api/ai/', include('ai.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/stats/', views.dashboard_stats, name='dashboard_stats'),
    path('api/settings/', views.get_system_settings, name='get_settings'),
    path('api/settings/save/', views.save_system_settings, name='save_settings'),
    # 前端静态资源
    re_path(r'^assets/(?P<path>.*)$', serve, {'document_root': BASE_DIR / 'dist/assets'}),
    # 所有其他路径都返回前端 index.html（让 Vue Router 接管）
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]