from django.db import models
from users.models import User

class ForumPost(models.Model):
    VISIBLE_CHOICES = (
        ('all', '公开'),
        ('student', '学生'),
        ('teacher', '老师'),
    )
    
    title = models.CharField(max_length=200, verbose_name='标题')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='作者')
    content = models.TextField(verbose_name='内容')
    post_date = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    status = models.CharField(max_length=20, default='approved', verbose_name='状态')
    visible_to = models.CharField(max_length=20, choices=VISIBLE_CHOICES, default='all', verbose_name='可见范围')
    views = models.IntegerField(default=0, verbose_name='浏览量')

    def __str__(self):
        return self.title

class ForumComment(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments', verbose_name='帖子')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_comments', verbose_name='作者')
    content = models.TextField(verbose_name='内容')
    comment_date = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
