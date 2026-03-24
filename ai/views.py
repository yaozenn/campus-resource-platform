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

    messages = [
        {"role": "system", "content": "你是一个智能学习助手，帮助学生解答学习相关的问题，提供学习建议和资源推荐。回答简洁友好。"},
        {"role": "user", "content": message}
    ]

    content, error = call_doubao(messages)
    if error:
        return Response({'response': f'AI 服务暂时不可用：{error}'})
    return Response({'response': content})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def teacher_insight(request):
    """
    教师端智能教学建议：
    根据该老师所有课程的浏览量、下载量、评论数、评论内容，
    让 AI 自动生成个性化教学建议。
    """
    from courses.models import Resource, ResourceComment

    user = request.user
    if user.role not in ('teacher', 'admin'):
        return Response({'error': '仅教师可用'}, status=403)

    # 拉取该老师的课程数据
    resources = Resource.objects.filter(uploader=user)

    if not resources.exists():
        return Response({
            'insight': '您目前还没有上传任何课程资源，快去上传第一份资源吧！上传后我会根据学生的反馈为您提供教学建议。',
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
        return Response({'insight': f'AI 分析暂时不可用：{error}', 'stats': course_stats})

    return Response({
        'insight': content,
        'stats': course_stats
    })