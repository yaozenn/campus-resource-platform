#!/usr/bin/env python3
"""
创建默认资源类型 (重构版 - 自动清理旧数据)
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_platform.settings')
django.setup()

from courses.models import ResourceType

def create_default_types():
    """创建并清理资源类型"""
    resource_categories = {
        '课程资源': [
            '课件/教案',
            '历年真题/试卷',
            '学霸笔记',
            '实验报告/数据'
        ],
        '网络资源': [
            '优质网课链接',
            '开源代码/项目',
            '实用软件/工具',
            '学术网站推荐'
        ],
        '书籍资源': [
            '电子版教材',
            '教辅/考研资料',
            '课外拓展读物',
            '二手书'
        ]
    }
    
    print('开始初始化/更新平台资源类型...')
    
    # 记录所有有效的新类型名称
    valid_type_names = []
    
    for main_category, sub_types in resource_categories.items():
        for type_name in sub_types:
            valid_type_names.append(type_name)
            type_obj, created = ResourceType.objects.get_or_create(
                name=type_name,
                defaults={'description': main_category}
            )
            if created:
                print(f'✅ 创建成功: [{main_category}] -> {type_name}')
            else:
                type_obj.description = main_category
                type_obj.save()
                print(f'🔄 已存在/更新: [{main_category}] -> {type_name}')

    # 自动清理：删除不在我们新列表里的所有旧类型
    old_types = ResourceType.objects.exclude(name__in=valid_type_names)
    deleted_count = old_types.count()
    if deleted_count > 0:
        old_types.delete()
        print(f'\n🗑️ 自动清理了 {deleted_count} 个废弃的旧类型！')
    
    print('\n🎉 资源类型重构完成！现在数据库里干干净净，只有我们设定好的 12 个分类了。')

if __name__ == '__main__':
    create_default_types()