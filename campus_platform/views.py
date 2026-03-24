from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.models import User
from courses.models import Resource, ResourceType
from forum.models import ForumPost
from announcements.models import Announcement
import json
from pathlib import Path

SETTINGS_FILE = Path(__file__).resolve().parent.parent / 'system_settings.json'

DEFAULT_SETTINGS = {
    'siteName': '校园课程资源共享平台',
    'siteDescription': '提供课程资源共享、学习交流的平台',
    'contactEmail': 'admin@campus.com',
    'allowRegister': True,
    'defaultRole': 'student',
    'initialPoints': 100,
    'dailySignPoints': 5,
    'uploadPoints': 20,
    'postPoints': 10,
    'commentPoints': 2,
    'enableCaptcha': False,
    'emailVerification': False,
    'minPasswordLength': 6,
    'smtpServer': 'smtp.qq.com',
    'smtpPort': 465,
    'smtpEmail': '',
    'smtpPassword': '',
    'enableEmailNotification': False,
    'enableSystemNotification': True,
    'notificationExpiryDays': 7,
    'enableAutoBackup': False,
    'backupFrequency': 'weekly',
    'dataRetentionDays': 30,
}


@api_view(['GET'])
@permission_classes([AllowAny])
def get_system_settings(request):
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # 补全缺失的默认字段（兼容旧配置文件）
        for k, v in DEFAULT_SETTINGS.items():
            if k not in data:
                data[k] = v
    else:
        data = DEFAULT_SETTINGS.copy()
    return JsonResponse({'success': True, 'settings': data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_system_settings(request):
    try:
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                current = json.load(f)
        else:
            current = DEFAULT_SETTINGS.copy()
        current.update(request.data)
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(current, f, ensure_ascii=False, indent=2)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_stats(request):
    try:
        total_users = User.objects.count()
        total_courses = Resource.objects.filter(status='active').count()
        total_posts = ForumPost.objects.filter(status='approved').count()
        total_points = sum(user.points for user in User.objects.all())

        students = User.objects.filter(role='student').count()
        teachers = User.objects.filter(role='teacher').count()
        admins = User.objects.filter(role='admin').count()

        pending_courses = Resource.objects.filter(status='pending').count()

        top_courses = Resource.objects.filter(status='active').order_by('-downloads')[:5]
        top_courses_data = []
        for course in top_courses:
            top_courses_data.append({
                'id': course.id,
                'title': course.title,
                'type': course.type.name if course.type else '未分类',
                'downloads': course.downloads,
                'points_required': course.points_required
            })

        return JsonResponse({
            'success': True,
            'stats': {
                'totalUsers': total_users,
                'totalCourses': total_courses,
                'totalPosts': total_posts,
                'totalPoints': total_points,
                'pendingCourses': pending_courses
            },
            'userDistribution': {
                'students': students,
                'teachers': teachers,
                'admins': admins
            },
            'topCourses': top_courses_data
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def home(request):
    html = '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>校园课程资源共享平台</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f0f2f5; margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
            .container { background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; max-width: 500px; width: 90%; }
            h1 { color: #1890ff; margin-bottom: 20px; }
            .api-item { list-style: none; padding: 8px 0; border-bottom: 1px solid #f0f0f0; text-align: left; }
            .api-item a { color: #1890ff; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>校园课程资源共享平台</h1>
            <p>后端 API 服务运行中</p>
            <ul style="padding:0;margin:20px 0">
                <li class="api-item">认证：<a href="/api/auth/">/api/auth/</a></li>
                <li class="api-item">课程：<a href="/api/courses/">/api/courses/</a></li>
                <li class="api-item">论坛：<a href="/api/forum/">/api/forum/</a></li>
                <li class="api-item">公告：<a href="/api/announcements/">/api/announcements/</a></li>
                <li class="api-item">积分：<a href="/api/points/">/api/points/</a></li>
                <li class="api-item">统计：<a href="/api/stats/">/api/stats/</a></li>
                <li class="api-item">系统设置：<a href="/api/settings/">/api/settings/</a></li>
                <li class="api-item">管理员：<a href="/admin/">/admin/</a></li>
            </ul>
        </div>
    </body>
    </html>
    '''
    return HttpResponse(html)