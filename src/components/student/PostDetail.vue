<template>
  <div class="page-container">
    <div class="back-btn" @click="goBack">
      <IconArrowLeft class="back-icon" /> 返回论坛
    </div>
    
    <div v-if="post" class="post-detail">
      <div class="post-header">
        <div class="post-title-section">
          <h1 class="post-title">{{ post.title }}</h1>
          <span v-if="isHot" class="hot-tag">
            <IconFlame class="hot-icon" /> 热门
          </span>
        </div>
        <div class="post-meta">
          <div class="meta-row">
            <IconUser class="meta-icon-svg" />
            <span class="meta-text">{{ post.author?.name || post.author?.username }}</span>
          </div>
          <div class="meta-row">
            <IconCalendar class="meta-icon-svg" />
            <span class="meta-text">{{ formatDateTime(post.post_date) }}</span>
          </div>
          <div class="meta-row">
            <IconEye class="meta-icon-svg" />
            <span class="meta-text">{{ post.views || 0 }} 次浏览</span>
          </div>
          <div class="meta-row">
            <IconMessage class="meta-icon-svg" />
            <span class="meta-text">{{ comments.length }} 条评论</span>
          </div>
          <span class="visible-tag">{{ getVisibleText(post.visible_to) }}</span>
        </div>
      </div>
      
      <div class="post-content">
        {{ post.content }}
      </div>
      
      <div class="post-actions">
        <button 
          v-if="canDelete" 
          @click="deletePost" 
          class="btn-delete"
        >
          <IconTrash class="btn-icon" /> 删除帖子
        </button>
      </div>
      
      <div class="comments-section">
        <div class="comments-header">
          <h3><IconMessage class="section-icon" /> 评论区</h3>
          <span class="comment-count">{{ comments.length }} 条评论</span>
        </div>
        
        <!-- 评论列表 -->
        <div class="comments-list">
          <div v-for="comment in comments" :key="comment.id" class="comment-item">
            <div class="comment-avatar">
              <div class="avatar-circle">
                {{ (comment.author?.name || comment.author?.username || 'U').charAt(0).toUpperCase() }}
              </div>
            </div>
            <div class="comment-body">
              <div class="comment-header">
                <div class="comment-author-section">
                  <span class="comment-author">{{ comment.author?.name || comment.author?.username }}</span>
                  <span class="comment-date">{{ formatDateTime(comment.comment_date) }}</span>
                </div>
              </div>
              <div class="comment-content">
                {{ comment.content }}
              </div>
            </div>
          </div>
          <div v-if="comments.length === 0" class="empty-state">
            <div class="empty-icon">
              <IconInbox class="empty-icon-svg" />
            </div>
            <p>暂无评论，快来抢沙发吧！</p>
          </div>
        </div>
        
        <!-- 发表评论 -->
        <div class="comment-form">
          <h4>发表评论</h4>
          <textarea 
            v-model="newComment" 
            placeholder="写下你的评论..." 
            rows="3"
            @keyup.ctrl.enter="submitComment"
          ></textarea>
          <div class="form-actions">
            <span class="form-tip">支持 Ctrl+Enter 快捷提交</span>
            <button @click="submitComment" class="btn-submit" :disabled="!newComment.trim() || submitting">
              {{ submitting ? '提交中...' : '发表评论' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { formatTime, formatDateTime } from '../../utils/timeFormat'
import { IconArrowLeft, IconFlame, IconUser, IconCalendar, IconEye, IconMessage, IconTrash, IconInbox } from '@/components/icons'

const route = useRoute()
const router = useRouter()
const post = ref<any>(null)
const comments = ref<any[]>([])
const newComment = ref('')
const submitting = ref(false)

const currentUser = computed(() => {
  return JSON.parse(localStorage.getItem('user') || '{}')
})

const canDelete = computed(() => {
  if (!post.value) return false
  const user = currentUser.value
  // 作者本人或管理员可以删除
  return user.id === post.value.author?.id || user.role === 'admin'
})

const isHot = computed(() => {
  if (!post.value) return false
  const views = post.value.views || 0
  const commentCount = comments.value.length
  return views > 100 || commentCount > 20
})

const getVisibleText = (visible: string) => {
  const map: any = { all: '公开', student: '学生', teacher: '老师' }
  return map[visible] || visible
}

const incrementViews = async () => {
  try {
    // 不需要 token，允许匿名访问
    await axios.post(
      `http://127.0.0.1:8000/api/forum/${route.params.id}/view/`,
      {}
    )
    // 更新本地浏览量显示
    if (post.value) {
      post.value.views = (post.value.views || 0) + 1
    }
  } catch (error) {
    console.error('增加浏览量失败', error)
  }
}

const fetchPost = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/forum/${route.params.id}/`)
    post.value = response.data
    // 获取帖子详情后增加浏览量
    await incrementViews()
  } catch (error) {
    console.error('获取帖子详情失败', error)
    alert('帖子不存在')
    goBack()
  }
}

const fetchComments = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/forum/${route.params.id}/comments/`)
    comments.value = response.data
  } catch (error) {
    console.error('获取评论失败', error)
  }
}

const submitComment = async () => {
  if (!newComment.value.trim()) return
  
  submitting.value = true
  try {
    const token = localStorage.getItem('token')
    await axios.post(
      `http://127.0.0.1:8000/api/forum/${route.params.id}/comments/`,
      { content: newComment.value },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    newComment.value = ''
    alert('评论成功')
    // 重新获取评论列表以显示最新评论
    await fetchComments()
  } catch (error: any) {
    console.error('评论失败', error)
    alert('评论失败：' + (error.response?.data?.message || '未知错误'))
  } finally {
    submitting.value = false
  }
}

const deletePost = async () => {
  if (!confirm('确定要删除这个帖子吗？')) return
  
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`http://127.0.0.1:8000/api/forum/${route.params.id}/delete/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    alert('删除成功')
    goBack()
  } catch (error) {
    alert('删除失败')
  }
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  fetchPost()
  fetchComments()
})
</script>

<style scoped>
.page-container {
  padding: var(--spacing-lg);
  max-width: 1000px;
  margin: 0 auto;
  background-color: var(--color-background);
  min-height: 100vh;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-secondary);
  transition: all var(--transition-fast);
  margin-bottom: 24px;
}

.back-btn:hover {
  background: var(--bg-secondary);
  border-color: var(--primary-color);
  color: var(--primary-color);
  transform: translateX(-4px);
}

.post-detail {
  background: var(--bg-primary);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-light);
}

.post-header {
  border-bottom: 2px solid var(--border-light);
  padding-bottom: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
}

.post-title-section {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.post-title {
  margin: 0;
  color: var(--text-primary);
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  line-height: 1.3;
  flex: 1;
}

.hot-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ff5252 100%);
  color: white;
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.post-meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-md);
  align-items: center;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.meta-icon {
  font-size: var(--font-size-base);
}

.back-icon {
  width: 16px;
  height: 16px;
}

.meta-icon-svg {
  width: 16px;
  height: 16px;
  color: var(--text-secondary);
}

.hot-icon {
  width: 14px;
  height: 14px;
}

.btn-icon {
  width: 16px;
  height: 16px;
}

.section-icon {
  width: 20px;
  height: 20px;
  margin-right: 8px;
  vertical-align: middle;
}

.empty-icon-svg {
  width: 64px;
  height: 64px;
  color: var(--text-placeholder);
}

.meta-text {
  color: var(--text-secondary);
}

.visible-tag {
  display: inline-block;
  padding: 4px 12px;
  background: var(--primary-light);
  color: var(--primary-color);
  border-radius: var(--border-radius);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  margin-left: auto;
}

.post-content {
  line-height: 1.8;
  color: var(--text-primary);
  white-space: pre-wrap;
  margin-bottom: var(--spacing-xl);
  padding: var(--spacing-lg);
  background: var(--bg-secondary);
  border-radius: var(--border-radius);
  font-size: var(--font-size-base);
}

.post-actions {
  border-top: 1px solid var(--border-light);
  padding-top: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.btn-delete {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #f56c6c 0%, #f78989 100%);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-fast);
  box-shadow: 0 2px 8px rgba(245, 108, 108, 0.3);
}

.btn-delete:hover {
  background: linear-gradient(135deg, #f78989 0%, #f56c6c 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(245, 108, 108, 0.4);
}

.comments-section {
  border-top: 1px solid var(--border-light);
  padding-top: var(--spacing-xl);
}

.comments-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.comments-header h3 {
  margin: 0;
  color: var(--text-primary);
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
}

.comment-count {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

.comments-list {
  margin-bottom: var(--spacing-xl);
}

.comment-item {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  background: var(--bg-secondary);
  border-radius: var(--border-radius);
  margin-bottom: var(--spacing-md);
  border: 1px solid var(--border-light);
  transition: all var(--transition-fast);
}

.comment-item:hover {
  border-color: var(--primary-light);
  box-shadow: var(--shadow-sm);
}

.comment-avatar {
  flex-shrink: 0;
}

.avatar-circle {
  width: 48px;
  height: 48px;
  border-radius: var(--border-radius-full);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  box-shadow: var(--shadow-sm);
}

.comment-body {
  flex: 1;
  min-width: 0;
}

.comment-header {
  margin-bottom: var(--spacing-sm);
}

.comment-author-section {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.comment-author {
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  font-size: var(--font-size-sm);
}

.comment-date {
  color: var(--text-placeholder);
  font-size: var(--font-size-xs);
}

.comment-content {
  line-height: 1.6;
  color: var(--text-primary);
  white-space: pre-wrap;
  font-size: var(--font-size-base);
}

.empty-state {
  text-align: center;
  color: var(--text-placeholder);
  padding: var(--spacing-xl);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: var(--spacing-md);
  opacity: 0.5;
}

.comment-form h4 {
  margin-bottom: var(--spacing-md);
  color: var(--text-primary);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
}

.comment-form textarea {
  width: 100%;
  padding: var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  resize: vertical;
  font-size: var(--font-size-base);
  margin-bottom: var(--spacing-md);
  transition: all var(--transition-fast);
  background: var(--bg-primary);
  color: var(--text-primary);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.comment-form textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--primary-light);
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-tip {
  color: var(--text-secondary);
  font-size: var(--font-size-xs);
}

.btn-submit {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 24px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  transition: all var(--transition-fast);
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3);
}

.btn-submit:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-color) 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  padding: var(--spacing-xl);
  color: var(--text-secondary);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto var(--spacing-md);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-container {
    padding: var(--spacing-md);
  }
  
  .post-detail {
    padding: var(--spacing-md);
  }
  
  .post-title {
    font-size: var(--font-size-xl);
  }
  
  .post-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }
  
  .visible-tag {
    margin-left: 0;
    margin-top: var(--spacing-sm);
  }
  
  .comment-item {
    flex-direction: column;
  }
  
  .comment-avatar {
    margin-bottom: var(--spacing-sm);
  }
}
</style>
