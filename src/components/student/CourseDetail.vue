<template>
  <div class="page-container">
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>
    
    <div v-else-if="!course" class="empty-state">
      <div class="empty-icon">📭</div>
      <p>资源不存在</p>
      <button @click="goBack" class="btn-back">返回</button>
    </div>
    
    <div v-else class="detail-page">
      <div class="back-btn" @click="goBack">
        <span>←</span> 返回列表
      </div>
      
      <div class="detail-content">
        <!-- 左侧：视频/封面区域 -->
        <div class="detail-left">
          <div class="media-section">
            <!-- 视频播放 -->
            <div v-if="isVideo" class="video-player">
              <video 
                :src="course.file_url" 
                controls 
                class="video-element"
                :poster="course.cover_image"
              >
                您的浏览器不支持视频播放
              </video>
            </div>
            
            <!-- 文档/其他类型显示封面 -->
            <div v-else class="cover-display">
              <div class="cover-placeholder">
                <span class="cover-icon">{{ getCoverIcon(course.type_name) }}</span>
              </div>
            </div>
            
            <!-- 下载按钮 -->
            <div class="download-section">
              <button @click="downloadCourse" class="btn-download">
                <span class="btn-icon">⬇</span>
                <span>下载资源</span>
              </button>
              <button @click="toggleCollect" :class="['btn-collect', isCollected ? 'active' : '']">
                <span class="btn-icon">{{ isCollected ? '★' : '☆' }}</span>
                <span>{{ isCollected ? '已收藏' : '收藏' }}</span>
              </button>
            </div>
          </div>
          
          <!-- 评论区 -->
          <div class="comments-section">
            <h3 class="section-title">💬 评论区 ({{ comments.length }})</h3>
            
            <!-- 发表评论 -->
            <div class="comment-form">
              <textarea 
                v-model="newComment" 
                placeholder="写下你的评论..." 
                class="comment-input"
                rows="3"
              ></textarea>
              <div class="comment-actions">
                <button @click="submitComment" class="btn-submit-comment" :disabled="submitting">
                  {{ submitting ? '提交中...' : '发表评论' }}
                </button>
              </div>
            </div>
            
            <!-- 评论列表 -->
            <div class="comments-list">
              <div v-for="comment in comments" :key="comment.id" class="comment-item">
                <div class="comment-avatar">
                  <div class="avatar-circle">
                    {{ comment.user?.name?.charAt(0) || comment.user?.username?.charAt(0) || 'U' }}
                  </div>
                </div>
                <div class="comment-body">
                  <div class="comment-header">
                    <span class="comment-author">{{ comment.user?.name || comment.user?.username }}</span>
                    <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
                  </div>
                  <p class="comment-content">{{ comment.content }}</p>
                </div>
              </div>
              <div v-if="comments.length === 0" class="no-comments">
                暂无评论，快来抢沙发吧！
              </div>
            </div>
          </div>
        </div>
        
        <!-- 右侧：信息区域 -->
        <div class="detail-right">
          <div class="info-card">
            <h1 class="course-title">{{ course.title }}</h1>
            
            <div class="course-meta">
              <div class="meta-item">
                <span class="meta-icon">🏷️</span>
                <span>{{ course.type_name || '未分类' }}</span>
              </div>
              <div class="meta-item">
                <span class="meta-icon">📥</span>
                <span>{{ course.downloads }} 次下载</span>
              </div>
              <div class="meta-item">
                <span class="meta-icon">👨‍🏫</span>
                <span>{{ course.uploader?.name || course.uploader?.username }}</span>
              </div>
              <div class="meta-item">
                <span class="meta-icon">📅</span>
                <span>{{ formatTime(course.upload_date) }}</span>
              </div>
            </div>
            
            <div class="course-description">
              <h3>📖 资源描述</h3>
              <p>{{ course.description || '暂无描述' }}</p>
            </div>
            
            <!-- 相关资源 -->
            <div v-if="relatedCourses.length > 0" class="related-section">
              <h3 class="section-title">📚 相关资源</h3>
              <div class="related-list">
                <div 
                  v-for="related in relatedCourses" 
                  :key="related.id" 
                  class="related-item"
                  @click="viewCourse(related.id)"
                >
                  <div class="related-info">
                    <h4>{{ related.title }}</h4>
                    <p>{{ related.type_name }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { formatTime } from '../../utils/timeFormat'

const route = useRoute()
const router = useRouter()

const course = ref<any>(null)
const loading = ref(true)
const isCollected = ref(false)
const comments = ref<any[]>([])
const newComment = ref('')
const submitting = ref(false)
const relatedCourses = ref<any[]>([])

const courseId = computed(() => route.params.id as string)

const isVideo = computed(() => {
  const videoTypes = ['视频', 'MOOC']
  return course.value && videoTypes.includes(course.value.type_name)
})

const getCoverIcon = (typeName: string) => {
  const iconMap: any = {
    '视频': '🎬',
    'MOOC': '🌐',
    '课件': '📊',
    '作业': '📝',
    '文档': '📄',
    '电子书': '📚'
  }
  return iconMap[typeName] || '📦'
}

const fetchCourseDetail = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/courses/${courseId.value}/`)
    course.value = response.data
  } catch (error) {
    console.error('获取课程详情失败', error)
  } finally {
    loading.value = false
  }
}

const fetchComments = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/courses/${courseId.value}/comments/`)
    comments.value = response.data
  } catch (error) {
    console.error('获取评论失败', error)
  }
}

const submitComment = async () => {
  if (!newComment.value.trim()) {
    alert('请输入评论内容')
    return
  }
  
  submitting.value = true
  try {
    const token = localStorage.getItem('token')
    await axios.post(
      `http://127.0.0.1:8000/api/courses/${courseId.value}/comments/`,
      { content: newComment.value },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    newComment.value = ''
    await fetchComments()
    alert('评论成功')
  } catch (error: any) {
    alert('评论失败：' + (error.response?.data?.message || '未知错误'))
  } finally {
    submitting.value = false
  }
}

const checkCollection = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/courses/collections/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    isCollected.value = response.data.some((c: any) => c.resource?.id === course.value?.id)
  } catch (error) {
    console.error('检查收藏状态失败', error)
  }
}

const toggleCollect = async () => {
  try {
    const token = localStorage.getItem('token')
    if (isCollected.value) {
      const collection = await axios.get('http://127.0.0.1:8000/api/courses/collections/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      const target = collection.data.find((c: any) => c.resource?.id === course.value?.id)
      if (target) {
        await axios.delete(`http://127.0.0.1:8000/api/courses/uncollect/${target.id}/`, {
          headers: { Authorization: `Bearer ${token}` }
        })
      }
      isCollected.value = false
      alert('已取消收藏')
    } else {
      await axios.post(
        'http://127.0.0.1:8000/api/courses/collect/',
        { resource: course.value?.id },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      isCollected.value = true
      alert('收藏成功')
    }
  } catch (error: any) {
    alert('操作失败：' + (error.response?.data?.message || '未知错误'))
  }
}

const downloadCourse = async () => {
  try {
    const token = localStorage.getItem('token')
    await axios.post(
      `http://127.0.0.1:8000/api/courses/${course.value.id}/download/`,
      {},
      { headers: { Authorization: `Bearer ${token}` } }
    )
    course.value.downloads += 1
    alert('下载成功！')
  } catch (error: any) {
    alert(error.response?.data?.error || '下载失败')
  }
}

const fetchRelatedCourses = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/courses/')
    const allCourses = response.data
    relatedCourses.value = allCourses
      .filter((c: any) => 
        c.type === course.value?.type && 
        c.id !== course.value?.id
      )
      .slice(0, 5)
  } catch (error) {
    console.error('获取相关资源失败', error)
  }
}

const goBack = () => {
  router.back()
}

const viewCourse = (id: string) => {
  router.push(`/student/courses/${id}`)
}

onMounted(() => {
  fetchCourseDetail()
  fetchComments()
  checkCollection()
  fetchRelatedCourses()
})
</script>

<style scoped>
.page-container {
  padding: var(--spacing-lg);
  background-color: var(--color-background);
  min-height: 100vh;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 100px 20px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 20px;
  opacity: 0.5;
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
  margin-bottom: 20px;
}

.back-btn:hover {
  background: var(--bg-secondary);
  border-color: var(--primary-color);
  color: var(--primary-color);
  transform: translateX(-4px);
}

.detail-page {
  max-width: 1400px;
  margin: 0 auto;
}

.detail-content {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: var(--spacing-lg);
}

.detail-left {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.media-section {
  background: var(--bg-primary);
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
}

.video-player {
  width: 100%;
  background: #000;
}

.video-element {
  width: 100%;
  max-height: 600px;
}

.cover-display {
  width: 100%;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.cover-placeholder {
  text-align: center;
}

.cover-icon {
  font-size: 120px;
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
}

.download-section {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  background: var(--bg-secondary);
}

.btn-download,
.btn-collect {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  transition: all var(--transition-fast);
}

.btn-download {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3);
}

.btn-download:hover {
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
  transform: translateY(-2px);
}

.btn-collect {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.btn-collect:hover {
  background: var(--bg-secondary);
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.btn-collect.active {
  background: linear-gradient(135deg, var(--success-color) 0%, var(--success-light) 100%);
  color: white;
  border-color: transparent;
  box-shadow: 0 2px 8px rgba(103, 194, 58, 0.3);
}

.btn-icon {
  font-size: var(--font-size-lg);
}

.comments-section {
  background: var(--bg-primary);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-md);
}

.section-title {
  margin: 0 0 var(--spacing-lg);
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
}

.comment-form {
  margin-bottom: var(--spacing-lg);
}

.comment-input {
  width: 100%;
  padding: var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: var(--font-size-base);
  resize: vertical;
  transition: all var(--transition-fast);
  background: var(--bg-primary);
  color: var(--text-primary);
}

.comment-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--primary-light);
}

.comment-actions {
  margin-top: var(--spacing-sm);
  text-align: right;
}

.btn-submit-comment {
  padding: 10px 24px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  transition: all var(--transition-fast);
}

.btn-submit-comment:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
}

.btn-submit-comment:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.comment-item {
  display: flex;
  gap: var(--spacing-md);
  padding-bottom: var(--spacing-lg);
  border-bottom: 1px solid var(--border-light);
}

.comment-item:last-child {
  border-bottom: none;
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
}

.comment-body {
  flex: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.comment-author {
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  font-size: var(--font-size-sm);
}

.comment-time {
  color: var(--text-placeholder);
  font-size: var(--font-size-xs);
}

.comment-content {
  margin: 0;
  color: var(--text-secondary);
  font-size: var(--font-size-base);
  line-height: 1.6;
}

.no-comments {
  text-align: center;
  color: var(--text-placeholder);
  padding: var(--spacing-lg);
}

.detail-right {
  position: sticky;
  top: 20px;
  height: fit-content;
}

.info-card {
  background: var(--bg-primary);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-md);
}

.course-title {
  margin: 0 0 var(--spacing-lg);
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  line-height: 1.3;
}

.course-meta {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-lg);
  border-bottom: 1px solid var(--border-light);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.meta-icon {
  font-size: var(--font-size-base);
}

.course-description {
  margin-bottom: var(--spacing-lg);
}

.course-description h3 {
  margin: 0 0 var(--spacing-md);
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.course-description p {
  margin: 0;
  color: var(--text-secondary);
  font-size: var(--font-size-base);
  line-height: 1.8;
}

.related-section {
  border-top: 1px solid var(--border-light);
  padding-top: var(--spacing-lg);
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.related-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: var(--spacing-md);
  background: var(--bg-secondary);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.related-item:hover {
  background: var(--bg-tertiary);
  transform: translateX(-4px);
}

.related-info {
  flex: 1;
}

.related-info h4 {
  margin: 0 0 6px;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.related-info p {
  margin: 0;
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
}

.related-points {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--warning-color);
  white-space: nowrap;
  margin-left: var(--spacing-md);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .detail-content {
    grid-template-columns: 1fr;
  }
  
  .detail-right {
    position: static;
  }
  
  .video-element {
    max-height: 300px;
  }
  
  .cover-display {
    height: 250px;
  }
  
  .cover-icon {
    font-size: 80px;
  }
  
  .download-section {
    flex-direction: column;
  }
}
</style>
