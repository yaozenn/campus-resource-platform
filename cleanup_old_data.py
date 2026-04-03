#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_platform.settings')
django.setup()

from courses.models import ResourceType, Resource, ResourceCollection

print('=== 清理前数据 ===')
print(f'资源总数: {Resource.objects.count()}')
print(f'收藏总数: {ResourceCollection.objects.count()}')

# 删除 type 为空的旧资源（ID 1-6）
invalid_resources = Resource.objects.filter(type__isnull=True)
print(f'\n删除 {invalid_resources.count()} 个无效资源...')
invalid_resources.delete()

# 删除关联这些资源的收藏
invalid_collections = ResourceCollection.objects.filter(resource__type__isnull=True)
print(f'删除 {invalid_collections.count()} 个无效收藏...')
invalid_collections.delete()

print('\n=== 清理后数据 ===')
print(f'资源总数: {Resource.objects.count()}')
print(f'收藏总数: {ResourceCollection.objects.count()}')

valid_resources = Resource.objects.all()
print(f'\n有效资源列表:')
for r in valid_resources:
    print(f'  ID: {r.id}, Title: {r.title}, Type: {r.type.name}')

print('\n✅ 数据清理完成！')
