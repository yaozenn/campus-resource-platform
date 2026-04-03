#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_platform.settings')
django.setup()

from courses.models import ResourceType, Resource, ResourceCollection

print('=== 资源类型 ===')
types = ResourceType.objects.all()
for t in types:
    print(f'  ID: {t.id}, Name: {t.name}, Desc: {t.description}')

print('\n=== 资源列表 ===')
resources = Resource.objects.all()
print(f'总资源数: {resources.count()}')
for r in resources:
    type_name = r.type.name if r.type else 'None'
    print(f'  ID: {r.id}, Title: {r.title[:30]}, Type: {type_name}, Status: {r.status}')

print('\n=== 收藏列表 ===')
collections = ResourceCollection.objects.all()
print(f'总收藏数: {collections.count()}')
for c in collections:
    resource_title = c.resource.title[:20] if c.resource else 'None'
    print(f'  ID: {c.id}, Resource: {resource_title}, User: {c.user.username}')
