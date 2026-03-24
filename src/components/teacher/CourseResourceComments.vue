<template>
  <div class="page-container">
    <h2>评论回复</h2>

    <div v-if="!selectedResource" class="resource-list">
      <div v-for="resource in resources" :key="resource.id" class="resource-item" @click="selectResource(resource)">
        <div class="resource-title">{{ resource.title }}</div>
        <div class="resource-meta">
          <span class="tag">{{ resource.type?.name || '未分类' }}</span>
          <span class="comment-count">💬 {{ resource.comment_count || 0 }} 条评论</span>
        </div>
      </div>
      <div v-if="resources.length === 0" class="empty-state">暂无资源</div>
    </div>

    <div v-else class="comment-section">
      <div class="back-bar">
        <button @click="selectedResource = null" class="btn-back">← 返回列表</button>
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
        <div v-if="comments.length === 0" class="empty-state">该资源暂无评论</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

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
.resource-list { display: flex; flex-direction: column; gap: 12px; }
.resource-item { background: white; padding: 16px 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); cursor: pointer; transition: all 0.2s; display: flex; justify-content: space-between; align-items: center; }
.resource-item:hover { box-shadow: 0 4px 12px rgba(64,158,255,0.2); border-left: 3px solid #409eff; }
.resource-title { font-weight: 600; color: #333; }
.resource-meta { display: flex; gap: 12px; align-items: center; }
.tag { background: #e6f7ff; color: #1890ff; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.comment-count { color: #999; font-size: 13px; }
.back-bar { display: flex; align-items: center; gap: 16px; margin-bottom: 20px; }
.btn-back { padding: 6px 14px; background: #f4f4f5; border: none; border-radius: 4px; cursor: pointer; color: #606266; }
.resource-name { font-weight: 600; font-size: 16px; color: #333; }
.comment-list { display: flex; flex-direction: column; gap: 16px; }
.comment-item { background: white; padding: 16px 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.comment-header { display: flex; justify-content: space-between; margin-bottom: 8px; }
.comment-user { font-weight: 600; color: #333; }
.comment-time { color: #999; font-size: 13px; }
.comment-content { color: #555; line-height: 1.6; margin-bottom: 12px; }
.reply-box { background: #f0f9eb; border-left: 3px solid #67c23a; padding: 10px 14px; border-radius: 4px; color: #555; }
.reply-label { color: #67c23a; font-weight: 600; margin-right: 6px; }
.reply-input-area { display: flex; gap: 10px; align-items: flex-end; }
.reply-input-area textarea { flex: 1; padding: 8px 12px; border: 1px solid #ddd; border-radius: 4px; resize: none; font-size: 14px; }
.btn-reply { padding: 8px 20px; background: #409eff; color: white; border: none; border-radius: 4px; cursor: pointer; white-space: nowrap; }
.empty-state { text-align: center; padding: 40px; color: #999; }
</style>