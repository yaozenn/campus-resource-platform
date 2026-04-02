from django.db import models, transaction
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', '管理员'),
        ('teacher', '教师'),
        ('student', '学生'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student', verbose_name='角色')
    avatar = models.URLField(blank=True, verbose_name='头像地址')
    bio = models.TextField(blank=True, verbose_name='个人简介')
    points = models.IntegerField(default=0, verbose_name='积分')
    
    # 额外字段
    student_id = models.CharField(max_length=20, blank=True, verbose_name='学号')
    employee_id = models.CharField(max_length=20, blank=True, verbose_name='教工号')
    real_name = models.CharField(max_length=50, blank=True, verbose_name='真实姓名')
    department = models.CharField(max_length=100, blank=True, verbose_name='院系/部门')
    phone = models.CharField(max_length=20, blank=True, verbose_name='手机号')
    gender = models.CharField(max_length=10, choices=(('male', '男'), ('female', '女'), ('other', '其他')), default='other', verbose_name='性别')
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='students', verbose_name='导师')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def add_points(self, amount, change_type, description=""):
        """
        统一的积分变动方法（支持事务和流水记录）
        """
        from points.models import PointRecord # 局部引入避免循环引用
        with transaction.atomic():
            self.points = (self.points or 0) + amount
            self.save(update_fields=['points'])
            
            PointRecord.objects.create(
                user=self,
                change_amount=amount,
                balance_after=self.points,
                change_type=change_type,
                description=description
            )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"