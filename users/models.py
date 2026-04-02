from django.db import models, transaction
from django.db.models import F
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', '管理员'),
        ('teacher', '教师'),
        ('student', '学生'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student', verbose_name='角色')
    name = models.CharField(max_length=50, blank=True, default='', verbose_name='姓名')
    avatar = models.URLField(blank=True, verbose_name='头像地址')
    bio = models.TextField(blank=True, verbose_name='个人简介')
    points = models.IntegerField(default=0, verbose_name='积分')
    
    student_id = models.CharField(max_length=20, blank=True, verbose_name='学号')
    employee_id = models.CharField(max_length=20, blank=True, verbose_name='教工号')
    real_name = models.CharField(max_length=50, blank=True, verbose_name='真实姓名')
    department = models.CharField(max_length=100, blank=True, verbose_name='院系/部门')
    phone = models.CharField(max_length=20, blank=True, verbose_name='手机号')
    gender = models.CharField(max_length=10, choices=(('male', '男'), ('female', '女'), ('other', '其他')), default='other', verbose_name='性别')
    major = models.CharField(max_length=50, blank=True, default='', verbose_name='专业')
    grade = models.CharField(max_length=20, blank=True, default='', verbose_name='年级')
    subject = models.CharField(max_length=50, blank=True, default='', verbose_name='学科')
    signature = models.CharField(max_length=200, blank=True, default='', verbose_name='个性签名')
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='students', verbose_name='导师')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def add_points(self, amount, change_type, description=""):
        """
        统一的积分变动方法（使用 F 表达式防止并发冲突）
        """
        from points.models import PointRecord  # 局部引入避免循环引用
        
        with transaction.atomic():
            # 1. 核心修复：使用 F() 表达式在数据库层面进行原子加法，防止覆盖更新
            User.objects.filter(pk=self.pk).update(points=F('points') + amount)
            
            # 2. 刷新内存对象，获取数据库中更新后的真实分数值
            self.refresh_from_db()
            
            # 3. 创建积分流水记录
            PointRecord.objects.create(
                user=self,
                change_amount=amount,
                balance_after=self.points,
                change_type=change_type,
                description=description
            )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"