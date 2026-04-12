from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

DOUBAO_API_KEY = os.getenv('DOUBAO_API_KEY', '')
DOUBAO_ENDPOINT_ID = os.getenv('DOUBAO_ENDPOINT_ID', '')


def call_doubao(messages, max_tokens=800):
    """统一调用豆包 API"""
    if not DOUBAO_ENDPOINT_ID:
        return None, 'AI 服务未配置 DOUBAO_ENDPOINT_ID'

    if DOUBAO_ENDPOINT_ID.startswith('bot-'):
        url = "https://ark.cn-beijing.volces.com/api/v3/bots/chat/completions"
    else:
        url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"

    payload = {
        "model": DOUBAO_ENDPOINT_ID,
        "messages": messages,
        "temperature": 0.8,
        "max_tokens": max_tokens
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {DOUBAO_API_KEY}'
    }

    try:
        resp = requests.post(url, data=json.dumps(payload), headers=headers, timeout=30)
        result = resp.json()
        if resp.status_code == 200:
            return result['choices'][0]['message']['content'], None
        else:
            return None, f'API 错误：{result}'
    except Exception as e:
        return None, str(e)


@api_view(['POST'])
def chat(request):
    """学生端通用问答"""
    message = request.data.get('message', '')
    if not message:
        return Response({'error': 'Message is required'}, status=400)

    # 先尝试调用API
    messages = [
        {"role": "system", "content": "你是一个智能学习助手，帮助学生解答学习相关的问题，提供学习建议和资源推荐。回答简洁友好。"},
        {"role": "user", "content": message}
    ]

    content, error = call_doubao(messages)
    if error:
        # API调用失败，使用fallback逻辑
        return Response({'response': generate_fallback_response(message)})
    return Response({'response': content})


def generate_fallback_response(message):
    """生成fallback响应，当API不可用时使用"""
    message_lower = message.lower()
    
    # 根据问题类型给出不同的回答
    if any(keyword in message_lower for keyword in ['推荐', '学习资源', '资源', '课程']):
        return """📚 学习资源推荐：

1. **平台内资源**：去「课程广场」看看，有很多优质教学资源！
2. **学习方法**：制定学习计划，每天坚持1-2小时
3. **互动学习**：多参与论坛讨论，和同学一起进步

加油！你一定可以的！💪"""
    
    elif any(keyword in message_lower for keyword in ['如何', '怎么', '怎样', '学习方法', '高效']):
        return """✨ 高效学习方法：

1. **番茄工作法**：学习25分钟，休息5分钟
2. **主动回忆**：学完后试着复述内容
3. **间隔重复**：定期复习巩固知识
4. **费曼技巧**：用简单的话讲给别人听

祝你学习进步！🚀"""
    
    elif any(keyword in message_lower for keyword in ['学习情况', '学习进度', '我的学习', '分析']):
        return """📊 学习分析建议：

1. **查看学习记录**：去「我的课程」看看已下载的资源
2. **参与互动**：多评论、多收藏喜欢的资源
3. **签到打卡**：每天签到可以获得积分哦
4. **设定目标**：每周学习2-3个新课程

坚持就是胜利！🎉"""
    
    elif any(keyword in message_lower for keyword in ['你好', 'hello', 'hi', '嗨']):
        return """👋 你好呀！我是你的AI学习助手！

我可以帮你：
- 📚 推荐学习资源
- 💡 解答学习问题
- 📊 分析学习情况
- ✨ 提供学习建议

有什么我可以帮你的吗？😊"""
    
    elif any(keyword in message_lower for keyword in ['谢谢', '感谢', 'thanks']):
        return """不客气！😊 能帮到你我很开心！

如果还有其他问题，随时来找我哦！加油！💪"""
    
    else:
        return f"""🤔 关于「{message}」：

这是个好问题！建议你：
1. 去「课程广场」搜索相关资源
2. 在论坛发帖和同学讨论
3. 查看已下载的课程资料

如果有具体的学习问题，随时告诉我！我会尽力帮你！💪"""


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def teacher_insight(request):
    """
    教师端智能教学建议：
    根据该老师所有课程的浏览量、下载量、评论数、评论内容，
    让 AI 自动生成个性化教学建议。
    """
    import logging
    logger = logging.getLogger(__name__)
    
    from courses.models import Resource, ResourceComment

    user = request.user
    logger.info(f"教师 {user.username} 请求AI教学建议")
    
    if user.role not in ('teacher', 'admin'):
        return Response({'error': '仅教师可用'}, status=403)

    # 拉取该老师的课程数据
    resources = Resource.objects.filter(uploader=user)
    logger.info(f"找到 {resources.count()} 个课程资源")

    if not resources.exists():
        return Response({
            'insight': '👋 欢迎使用智能教学助手！\n\n您目前还没有上传任何课程资源。建议您：\n\n1. 先上传第一份教学资源\n2. 引导学生下载和评论\n3. 之后再来获取个性化教学建议\n\n期待您的精彩课程！',
            'stats': []
        })

    # 构建课程数据摘要
    course_stats = []
    data_lines = []

    for r in resources:
        comments = ResourceComment.objects.filter(resource=r)
        comment_count = comments.count()
        # 取最近5条评论内容
        recent_comments = list(comments.order_by('-comment_date').values_list('content', flat=True)[:5])

        course_stats.append({
            'id': r.id,
            'title': r.title,
            'downloads': r.downloads,
            'comment_count': comment_count,
            'status': r.status,
            'recent_comments': recent_comments
        })

        line = f"- 《{r.title}》：下载 {r.downloads} 次，{comment_count} 条评论"
        if recent_comments:
            line += f"，最近评论摘要：{'；'.join(recent_comments[:3])}"
        data_lines.append(line)

    data_summary = "\n".join(data_lines)
    logger.info(f"课程数据摘要准备完成")
    
    # 检查API密钥
    api_key = os.getenv('DOUBAO_API_KEY', '')
    endpoint_id = os.getenv('DOUBAO_ENDPOINT_ID', '')
    logger.info(f"API密钥状态: {'已设置' if api_key else '未设置'}, 端点ID: {endpoint_id if endpoint_id else '未设置'}")

    system_prompt = """你是一位经验丰富、亲切友好的教学顾问，专门帮助大学教师改进教学质量。
你会根据课程数据（下载量、评论数、评论内容）给出具体、实用、温暖的教学建议。
要求：
1. 语气亲切自然，像朋友聊天，不要太正式
2. 建议要具体，结合实际数据
3. 可以适当使用emoji让建议更生动
4. 针对不同情况给出不同建议：
   - 下载多但评论少：可能学生在默默消化，建议鼓励互动
   - 评论多且有疑问：说明难点较多，建议补充讲解
   - 下载少：可能需要提升资源吸引力或宣传
   - 课程表现好：给予鼓励并建议保持或拓展
5. 结尾给出1-2条具体可执行的建议
6. 回复长度适中，200-350字"""

    user_prompt = f"""以下是我的课程数据，请给我一些教学建议：

{data_summary}

请根据以上数据，给我个性化的教学反馈和改进建议。"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    content, error = call_doubao(messages, max_tokens=600)
    if error:
        fallback_insight = generate_fallback_insight(course_stats)
        return Response({
            'insight': fallback_insight,
            'stats': course_stats
        })

    return Response({
        'insight': content,
        'stats': course_stats
    })


def generate_fallback_insight(stats):
    """生成模拟的教学建议（当AI服务不可用时）"""
    if not stats:
        return '您目前还没有上传任何课程资源，快去上传第一份资源吧！上传后我会根据学生的反馈为您提供教学建议。'
    
    total_downloads = sum(c['downloads'] for c in stats)
    total_comments = sum(c['comment_count'] for c in stats)
    course_count = len(stats)
    
    insights = []
    insights.append(f"📊 您目前共有 {course_count} 门课程，总计获得 {total_downloads} 次下载和 {total_comments} 条评论！")
    
    if total_downloads > 100:
        insights.append("🎉 您的课程非常受欢迎！学生们都很喜欢您的教学资源。继续保持这种高质量的内容输出！")
    elif total_downloads > 20:
        insights.append("👍 您的课程正在稳步发展，建议可以多在班级群或平台上推广一下，让更多学生受益！")
    else:
        insights.append("💡 您的课程刚起步，建议可以完善一下课程描述和封面，或者在课堂上引导学生下载使用。")
    
    if total_comments > 10:
        insights.append("💬 学生们的互动很活跃！建议您定期查看评论区，及时回应学生的疑问，这对提升教学效果很有帮助。")
    elif total_comments > 0:
        insights.append("💬 有一些学生评论了，建议您可以鼓励更多学生分享学习心得，形成良好的学习氛围。")
    
    insights.append("\n📝 具体建议：")
    insights.append("1. 定期更新教学资源，保持内容的时效性")
    insights.append("2. 主动与学生互动，收集反馈并改进教学")
    insights.append("3. 可以录制一些简短的讲解视频，帮助学生理解难点")
    
    return "\n".join(insights)