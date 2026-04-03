#!/usr/bin/env python3
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_platform.settings')
django.setup()

from users.models import User

test_users = [
    ('admin', 'admin', 'admin123'),
    ('s1', 'student', 's123'),
    ('t1', 'teacher', 't123'),
]

for username, role, password in test_users:
    try:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f'✅ 已重置用户 {username} (角色: {role}) 的密码为: {password}')
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            password=password,
            role=role,
            name=username
        )
        print(f'✅ 已创建用户 {username} (角色: {role})，密码: {password}')

print('\n测试账号信息：')
print('管理员: admin / admin123')
print('学生: s1 / s123')
print('教师: t1 / t123')
