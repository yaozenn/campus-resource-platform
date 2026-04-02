from django.db import models
from users.models import User

class ResourceType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='资源类型名称')
    description = models.TextField(blank=True, verbose_name='类型描述')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Resource(models.Model):
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
        ('active', '已发布'),
    )
    
    title = models.CharField(max_length=200, verbose_name='资源名称')
    type = models.ForeignKey(ResourceType, on_delete=models.SET_NULL, null=True, related_name='resources', verbose_name='资源类型')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_resources', verbose_name='上传用户')
    description = models.TextField(blank=True, verbose_name='资源描述')
    file_url = models.URLField(blank=True, verbose_name='文件地址')
    cover_image = models.URLField(blank=True, verbose_name='封面图片')
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name='上传日期')
    downloads = models.IntegerField(default=0, verbose_name='下载次数')
    points_required = models.IntegerField(default=0, verbose_name='所需积分')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    reject_reason = models.TextField(blank=True, verbose_name='拒绝原因')
    is_second_hand = models.BooleanField(default=False, verbose_name='是否二手')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='价格')
    
    # 新增高级功能字段
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0, verbose_name='资源评分')
    rating_count = models.IntegerField(default=0, verbose_name='评分人数')

    def __str__(self):
        return self.title

class ResourceComment(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_comments')
    content = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    reply = models.TextField(blank=True)
    user_rating = models.IntegerField(default=5, verbose_name='用户评分')

    def __str__(self):
        return f"Comment by {self.user.username} on {self.resource.title}"

class ResourceCollection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='collected_by')
    collect_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'resource')

    def __str__(self):
        return f"{self.user.username} collected {self.resource.title}"

class ResourceReport(models.Model):
    REASON_CHOICES = (
        ('ad', '垃圾广告'),
        ('copy', '侵权内容'),
        ('bad', '内容违规'),
        ('other', '其他原因'),
    )
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='reports', verbose_name='举报资源')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='举报人')
    reason = models.CharField(max_length=20, choices=REASON_CHOICES, verbose_name='举报原因')
    description = models.TextField(blank=True, verbose_name='详细说明')
    status = models.CharField(max_length=20, default='pending', choices=(
        ('pending', '待处理'),
        ('resolved', '已处理'),
        ('ignored', '已忽略'),
    ), verbose_name='处理状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='举报时间')