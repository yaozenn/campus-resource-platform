<template>
  <div class="page-container">
    <h2>评论回复</h2>

    <div v-if="!selectedResource" class="resource-list">
      <div v-for="resource in resources" :key="resource.id" class="resource-item" @click="selectResource(resource)">
        <div class="resource-title">{{ resource.title }}</div>
        <div class="resource-meta">
          <span class="tag">{{ resource.type?.name || '未分类' }}</span>
          <span class="comment-count">
            <IconMessage class="comment-icon" />
            {{ resource.comment_count || 0 }} 条评论
          </span>
        </div>
      </div>
      <div v-if="resources.length === 0" class="empty-state">
        <IconFolder class="empty-icon" />
        <p>暂无资源</p>
      </div>
    </div>

    <div v-else class="comment-section">
      <div class="back-bar">
        <button @click="selectedResource = null" class="btn-back">
          <IconArrowLeft class="back-icon" />
          返回列表
        </button>
        <span class="resource-name">{{ selectedResource.title }}</span>
      </div>

      <div class="comment-list">
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <div class="comment-header">
            <span class="comment-user">{{ comment.user?.name || comment.user?.username }}</span>
            <span class="comment-time">{{ formatDate(comment.comment_date) }}</span>
          </div>
          <div class="comment-content">{{ comment.content }}</div>

          <div v-if="comment.reply" class="reply-box">
            <span class="reply-label">老师回复：</span>{{ comment.reply }}
          </div>

          <div v-else class="reply-input-area">
            <textarea v-model="replyMap[comment.id]" placeholder="输入回复内容..." rows="2"></textarea>
            <button @click="submitReply(comment)" class="btn-reply">回复</button>
          </div>
        </div>
        <div v-if="comments.length === 0" class="empty-state">
          <IconMessage class="empty-icon" />
          <p>该资源暂无评论</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { IconMessage, IconFolder, IconArrowLeft } from '../../components/icons'

const resources = ref<any[]>([])
const selectedResource = ref<any>(null)
const comments = ref<any[]>([])
const replyMap = ref<Record<number, string>>({})

const formatDate = (d: string) => new Date(d).toLocaleString('zh-CN')

const fetchResources = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('http://127.0.0.1:8000/api/courses/teacher/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    resources.value = res.data
  } catch (e) {
    console.error('获取资源失败', e)
  }
}

const selectResource = async (resource: any) => {
  selectedResource.value = resource
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get(`http://127.0.0.1:8000/api/courses/${resource.id}/comments/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    comments.value = res.data
  } catch (e) {
    console.error('获取评论失败', e)
  }
}

const submitReply = async (comment: any) => {
  const replyContent = replyMap.value[comment.id]
  if (!replyContent?.trim()) return alert('回复内容不能为空')
  try {
    const token = localStorage.getItem('token')
    await axios.patch(`http://127.0.0.1:8000/api/courses/${selectedResource.value.id}/comments/`, 
      { comment_id: comment.id, reply: replyContent },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    comment.reply = replyContent
    delete replyMap.value[comment.id]
    alert('回复成功')
  } catch (e) {
    alert('回复失败')
  }
}

onMounted(fetchResources)
</script>

<style scoped>
.page-container { padding: 20px; }
h2 { color: var(--text-primary); font-family: var(--font-sf); margin-bottom: 20px; }
.resource-list { display: flex; flex-direction: column; gap: 12px; }
.resource-item { 
  background: white; 
  padding: 16px 20px; 
  border-radius: var(--border-radius-lg); 
  box-shadow: var(--shadow-sm); 
  cursor: pointer; 
  transition: all var(--transition-fast); 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  border: 1px solid var(--border-light);
}
.resource-item:hover { 
  box-shadow: var(--shadow-md); 
  border-left: 3px solid var(--primary-color); 
}
.resource-title { font-weight: 600; color: var(--text-primary); }
.resource-meta { display: flex; gap: 12px; align-items: center; }
.tag { 
  background: rgba(13, 148, 136, 0.1); 
  color: var(--primary-color); 
  padding: 4px 12px; 
  border-radius: 20px; 
  font-size: 12px; 
  font-weight: 500;
}
.comment-count { 
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--text-tertiary); 
  font-size: 13px; 
}
.comment-icon {
  width: 16px;
  height: 16px;
}
.back-bar { 
  display: flex; 
  align-items: center; 
  gap: 16px; 
  margin-bottom: 20px; 
}
.btn-back { 
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px; 
  background: var(--bg-tertiary); 
  border: none; 
  border-radius: var(--border-radius); 
  cursor: pointer; 
  color: var(--text-secondary); 
  font-weight: 500;
  transition: all var(--transition-fast);
}
.btn-back:hover {
  background: var(--bg-secondary);
  color: var(--primary-color);
}
.back-icon {
  width: 16px;
  height: 16px;
}
.resource-name { font-weight: 600; font-size: 16px; color: var(--text-primary); }
.comment-list { display: flex; flex-direction: column; gap: 16px; }
.comment-item { 
  background: white; 
  padding: 16px 20px; 
  border-radius: var(--border-radius-lg); 
  box-shadow: var(--shadow-sm); 
  border: 1px solid var(--border-light);
}
.comment-header { display: flex; justify-content: space-between; margin-bottom: 8px; }
.comment-user { font-weight: 600; color: var(--text-primary); }
.comment-time { color: var(--text-tertiary); font-size: 13px; }
.comment-content { color: var(--text-secondary); line-height: 1.6; margin-bottom: 12px; }
.reply-box { 
  background: rgba(16, 185, 129, 0.05); 
  border-left: 3px solid var(--success-color); 
  padding: 10px 14px; 
  border-radius: 4px; 
  color: var(--text-secondary); 
}
.reply-label { color: var(--success-color); font-weight: 600; margin-right: 6px; }
.reply-input-area { display: flex; gap: 10px; align-items: flex-end; }
.reply-input-area textarea { 
  flex: 1; 
  padding: 10px 14px; 
  border: 1px solid var(--border-color); 
  border-radius: var(--border-radius); 
  resize: none; 
  font-size: 14px; 
  transition: all var(--transition-fast);
}
.reply-input-area textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
}
.btn-reply { 
  padding: 10px 24px; 
  background: var(--primary-color); 
  color: white; 
  border: none; 
  border-radius: var(--border-radius); 
  cursor: pointer; 
  white-space: nowrap; 
  font-weight: 500;
  transition: all var(--transition-fast);
}
.btn-reply:hover {
  background: var(--primary-dark);
}
.empty-state { 
  text-align: center; 
  padding: 40px; 
  color: var(--text-tertiary); 
}
.empty-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto 12px;
  color: var(--text-tertiary);
}
</style>
