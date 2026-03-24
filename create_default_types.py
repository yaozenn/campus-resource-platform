#!/usr/bin/env python3
"""
创建默认资源类型
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_platform.settings')
django.setup()

from courses.models import ResourceType

def create_default_types():
    """创建默认资源类型"""
    default_types = [
        '课程资源',
        '二手书',
        '电子书',
        '其他'
    ]
    
    for type_name in default_types:
        type_obj, created = ResourceType.objects.get_or_create(name=type_name)
        if created:
            print(f'创建类型: {type_name}')
        else:
            print(f'类型已存在: {type_name}')

if __name__ == '__main__':
    create_default_types()
    print('默认资源类型创建完成！')
