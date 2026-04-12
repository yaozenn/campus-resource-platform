from django.db import models
from django.utils import timezone
from users.models import User

class CheckInRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkin_records', verbose_name='用户')
    checkin_date = models.DateField(verbose_name='签到日期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '签到记录'
        verbose_name_plural = verbose_name
        ordering = ['-checkin_date', '-created_at']
        unique_together = [('user', 'checkin_date')]

    def __str__(self):
        return f"{self.user.username} - {self.checkin_date}"

class PointRecord(models.Model):
    CHANGE_TYPE_CHOICES = (
        ('checkin', '每日签到'),
        ('upload', '资源上传奖励'),
        ('post', '论坛发帖奖励'),
        ('exchange', '礼品兑换扣除'),
        ('admin', '管理员操作'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='point_records', verbose_name='用户')
    change_amount = models.IntegerField(verbose_name='变动额度') # 正数加分，负数扣分
    balance_after = models.IntegerField(verbose_name='变动后余额')
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPE_CHOICES, verbose_name='变动类型')
    description = models.CharField(max_length=255, blank=True, verbose_name='备注说明')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '积分流水'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username} - {self.change_type}: {self.change_amount}"

class Prize(models.Model):
    name = models.CharField(max_length=100, verbose_name='奖品名称')
    description = models.TextField(verbose_name='奖品描述')
    points_required = models.IntegerField(verbose_name='所需积分')
    stock = models.IntegerField(default=0, verbose_name='库存')
    image_url = models.URLField(blank=True, verbose_name='奖品图片')
    is_active = models.BooleanField(default=True, verbose_name='是否上架')

    def __str__(self):
        return self.name

class PrizeExchange(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='兑换用户')
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE, verbose_name='兑换奖品')
    exchange_date = models.DateTimeField(auto_now_add=True, verbose_name='兑换日期')
    status = models.CharField(max_length=20, default='pending', verbose_name='处理状态')

    def __str__(self):
        return f"{self.user.username} exchanged {self.prize.name}"