import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_platform.settings')
django.setup()

from users.models import User
from points.models import Prize
from forum.models import ForumPost
from announcements.models import Announcement
from courses.models import CourseResource, CourseType


def init_test_data():
    print('开始初始化测试数据...')
    
    # 创建管理员
    admin, _ = User.objects.get_or_create(
        username='admin',
        defaults={
            'name': '系统管理员',
            'role': 'admin',
            'phone': '13800000000',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if _:
        admin.set_password('admin123')
        admin.save()
    print('✓ 管理员账号已创建')
    
    # 创建老师账号
    teachers_data = [
        {'username': 'teacher101', 'name': '张教授', 'employee_id': '101', 'gender': 'male', 'phone': '13800000101', 'subject': '计算机科学', 'department': '计算机学院', 'points': 500},
        {'username': 'teacher102', 'name': '李老师', 'employee_id': '102', 'gender': 'female', 'phone': '13800000102', 'subject': '数学', 'department': '理学院', 'points': 450},
        {'username': 'teacher103', 'name': '王副教授', 'employee_id': '103', 'gender': 'male', 'phone': '13800000103', 'subject': '英语', 'department': '外国语学院', 'points': 480},
    ]
    
    for data in teachers_data:
        teacher, created = User.objects.get_or_create(username=data['username'], defaults=data)
        if created:
            teacher.set_password('teacher123')
            teacher.role = 'teacher'
            teacher.save()
    print('✓ 3个老师账号已创建')
    
    # 创建学生账号
    students_data = [
        {'username': 'student1001', 'name': '小明', 'student_id': '1001', 'gender': 'male', 'phone': '13900001001', 'major': '计算机科学与技术', 'grade': '2021级', 'points': 200, 'signature': '学习使我快乐'},
        {'username': 'student1002', 'name': '小红', 'student_id': '1002', 'gender': 'female', 'phone': '13900001002', 'major': '软件工程', 'grade': '2021级', 'points': 180, 'signature': '代码改变世界'},
        {'username': 'student1003', 'name': '小刚', 'student_id': '1003', 'gender': 'male', 'phone': '13900001003', 'major': '人工智能', 'grade': '2022级', 'points': 150, 'signature': 'AI爱好者'},
        {'username': 'student1004', 'name': '小丽', 'student_id': '1004', 'gender': 'female', 'phone': '13900001004', 'major': '数据科学', 'grade': '2022级', 'points': 160, 'signature': '数据分析达人'},
        {'username': 'student1005', 'name': '小强', 'student_id': '1005', 'gender': 'male', 'phone': '13900001005', 'major': '网络安全', 'grade': '2020级', 'points': 220, 'signature': '安全守护者'},
        {'username': 'student1006', 'name': '小芳', 'student_id': '1006', 'gender': 'female', 'phone': '13900001006', 'major': '计算机科学与技术', 'grade': '2020级', 'points': 190, 'signature': '全栈开发'},
        {'username': 'student1007', 'name': '小华', 'student_id': '1007', 'gender': 'male', 'phone': '13900001007', 'major': '软件工程', 'grade': '2023级', 'points': 100, 'signature': '新手上路'},
        {'username': 'student1008', 'name': '小敏', 'student_id': '1008', 'gender': 'female', 'phone': '13900001008', 'major': '人工智能', 'grade': '2023级', 'points': 120, 'signature': '深度学习'},
    ]
    
    for data in students_data:
        student, created = User.objects.get_or_create(username=data['username'], defaults=data)
        if created:
            student.set_password('student123')
            student.role = 'student'
            student.save()
    print('✓ 8个学生账号已创建')
    
    # 创建奖品
    prizes_data = [
        {'name': '笔记本', 'description': '精美笔记本一本', 'points_required': 50, 'stock': 100, 'is_active': True},
        {'name': 'U盘', 'description': '32GB U盘一个', 'points_required': 150, 'stock': 50, 'is_active': True},
        {'name': '保温杯', 'description': '智能保温杯一个', 'points_required': 200, 'stock': 30, 'is_active': True},
        {'name': '充电宝', 'description': '10000mAh充电宝', 'points_required': 300, 'stock': 20, 'is_active': True},
        {'name': '蓝牙耳机', 'description': '无线蓝牙耳机一副', 'points_required': 500, 'stock': 10, 'is_active': True},
    ]
    
    for data in prizes_data:
        Prize.objects.get_or_create(name=data['name'], defaults=data)
    print('✓ 5个奖品已创建')
    
    # 创建课程类型
    course_types = ['视频教程', 'PPT课件', '实验报告', '期末复习', '其他资料']
    for type_name in course_types:
        CourseType.objects.get_or_create(name=type_name)
    print('✓ 5个课程类型已创建')
    
    # 创建论坛帖子
    posts_data = [
        {'title': 'Python入门学习心得', 'content': '大家好，我是新来的学生，最近在学习Python，感觉这门语言很有趣，想和大家分享一下我的学习心得...', 'author': User.objects.filter(role='student').first(), 'visible_to': 'all'},
        {'title': '高数期末考试重点', 'content': '整理了一些高数期末考试的重点知识，希望对大家有帮助...', 'author': User.objects.filter(role='teacher').first(), 'visible_to': 'student'},
        {'title': '毕业设计选题讨论', 'content': '各位老师同学，想讨论一下今年毕业设计的选题方向，欢迎大家发表意见...', 'author': User.objects.filter(role='teacher').first(), 'visible_to': 'all'},
    ]
    
    for data in posts_data:
        ForumPost.objects.get_or_create(title=data['title'], defaults=data)
    print('✓ 3个论坛帖子已创建')
    
    # 创建公告
    announcements_data = [
        {'title': '关于2024年春季学期选课的通知', 'content': '各位同学：2024年春季学期选课将于近期开始，请大家关注教务处网站通知...', 'author': admin, 'visible_to': 'all'},
        {'title': '图书馆延长开放时间', 'content': '为方便同学们复习备考，图书馆自即日起延长开放时间至晚11点...', 'author': admin, 'visible_to': 'student'},
        {'title': '教师教学研讨会通知', 'content': '各位老师：本周四下午3点在会议室召开教学研讨会，请准时参加...', 'author': admin, 'visible_to': 'teacher'},
    ]
    
    for data in announcements_data:
        Announcement.objects.get_or_create(title=data['title'], defaults=data)
    print('✓ 3个公告已创建')
    
    print('\n测试数据初始化完成！')
    print('账号信息：')
    print('  管理员: admin / admin123')
    print('  老师: teacher101~103 / teacher123')
    print('  学生: student1001~1008 / student123')


if __name__ == '__main__':
    init_test_data()
