from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', '管理员'),
        ('student', '学生'),
        ('teacher', '老师'),
    )
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
        ('other', '其他'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True, default=None)
    student_id = models.CharField(max_length=20, blank=True, verbose_name='学号')
    employee_id = models.CharField(max_length=20, blank=True, verbose_name='工号')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, verbose_name='性别')
    phone = models.CharField(max_length=20, blank=True, verbose_name='手机号')
    signature = models.CharField(max_length=200, blank=True, verbose_name='个性签名')
    major = models.CharField(max_length=50, blank=True, verbose_name='专业')
    grade = models.CharField(max_length=20, blank=True, verbose_name='年级')
    subject = models.CharField(max_length=50, blank=True, verbose_name='学科')
    department = models.CharField(max_length=50, blank=True, verbose_name='部门')
    points = models.IntegerField(default=0)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username
