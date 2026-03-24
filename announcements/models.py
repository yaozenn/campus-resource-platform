from django.db import models
from users.models import User

class Announcement(models.Model):
    VISIBLE_CHOICES = (
        ('all', '公开'),
        ('student', '学生'),
        ('teacher', '老师'),
    )
    
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements', verbose_name='发布者')
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    status = models.CharField(max_length=20, default='active', verbose_name='状态')
    visible_to = models.CharField(max_length=20, choices=VISIBLE_CHOICES, default='all', verbose_name='可见范围')

    def __str__(self):
        return self.title
