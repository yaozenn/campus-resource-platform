<template>
  <div class="page-container">
    <div class="back-btn" @click="goBack">
      <IconArrowLeft class="back-icon" /> 返回公告列表
    </div>
    
    <div v-if="announcement" class="announcement-detail">
      <div class="announcement-header">
        <h1>{{ announcement.title }}</h1>
        <div class="announcement-meta">
          <span class="author"><IconUser class="meta-icon" /> {{ announcement.author?.name || announcement.author?.username }}</span>
          <span class="date"><IconCalendar class="meta-icon" /> {{ formatDateTime(announcement.publish_date) }}</span>
        </div>
      </div>
      
      <div class="announcement-content">
        {{ announcement.content }}
      </div>
      
      <div v-if="canDelete" class="announcement-actions">
        <button @click="deleteAnnouncement" class="btn-delete">
          <IconTrash class="btn-icon" /> 删除公告
        </button>
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
import { formatDateTime } from '../../utils/timeFormat'
import { IconArrowLeft, IconUser, IconCalendar, IconTrash } from '../icons'

const route = useRoute()
const router = useRouter()
const announcement = ref<any>(null)

const currentUser = computed(() => {
  return JSON.parse(localStorage.getItem('user') || '{}')
})

const canDelete = computed(() => {
  if (!announcement.value) return false
  const user = currentUser.value
  // 作者本人或管理员可以删除
  return user.id === announcement.value.author?.id || user.role === 'admin'
})

const fetchAnnouncement = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/announcements/${route.params.id}/`)
    announcement.value = response.data
  } catch (error) {
    console.error('获取公告详情失败', error)
    alert('公告不存在')
    goBack()
  }
}

const deleteAnnouncement = async () => {
  if (!confirm('确定要删除这个公告吗？')) return
  
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`http://127.0.0.1:8000/api/announcements/${route.params.id}/`, {
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
  fetchAnnouncement()
})
</script>

<style scoped>
.page-container {
  padding: var(--spacing-lg);
  max-width: 900px;
  margin: 0 auto;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  cursor: pointer;
  margin-bottom: var(--spacing-lg);
  transition: all var(--transition-fast);
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.back-btn:hover {
  background: var(--bg-tertiary);
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.back-icon { width: 16px; height: 16px; }

.announcement-detail {
  background: var(--bg-primary);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-md);
}

.announcement-header {
  border-bottom: 2px solid var(--border-light);
  padding-bottom: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
}

.announcement-header h1 {
  margin: 0 0 var(--spacing-md);
  color: var(--text-primary);
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
}

.announcement-meta {
  display: flex;
  gap: var(--spacing-lg);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.announcement-meta span {
  display: flex;
  align-items: center;
  gap: 6px;
}

.meta-icon { width: 16px; height: 16px; }

.announcement-content {
  line-height: 1.8;
  color: var(--text-primary);
  white-space: pre-wrap;
  margin-bottom: var(--spacing-xl);
  padding: var(--spacing-lg);
  background: var(--bg-secondary);
  border-radius: var(--border-radius-md);
}

.announcement-actions {
  border-top: 1px solid var(--border-light);
  padding-top: var(--spacing-lg);
}

.btn-delete {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  background: var(--danger-color);
  color: white;
  border: none;
  border-radius: var(--border-radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

.btn-delete:hover {
  background: #f78989;
  transform: translateY(-2px);
}

.btn-icon { width: 16px; height: 16px; }

.loading {
  text-align: center;
  padding: 60px;
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
</style>
