from django.db import models
from users.models import User

class PointsRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points_records')
    type = models.CharField(max_length=20, choices=[('add', '增加'), ('deduct', '扣除')])
    points = models.IntegerField()
    reason = models.CharField(max_length=200)
    record_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.type} {self.points} points"

class Prize(models.Model):
    name = models.CharField(max_length=100, verbose_name='奖品名称')
    description = models.TextField(blank=True, verbose_name='奖品描述')
    points_required = models.IntegerField(verbose_name='所需积分')
    stock = models.IntegerField(default=0, verbose_name='库存数量')
    image = models.URLField(blank=True, verbose_name='奖品图片')
    is_active = models.BooleanField(default=True, verbose_name='是否上架')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PrizeExchange(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prize_exchanges')
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE, related_name='exchanges')
    points_spent = models.IntegerField()
    status = models.CharField(max_length=20, default='pending', 
                            choices=[('pending', '待处理'), ('approved', '已通过'), ('rejected', '已拒绝')])
    exchange_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} 兑换 {self.prize.name}"
