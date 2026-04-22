<template>
  <div class="page-container fade-in">
    <div class="page-header">
      <div class="header-content">
        <h2>
          <IconCollection class="header-icon" />
          我的收藏
        </h2>
        <p class="subtitle">管理你收藏的所有学习资源</p>
      </div>
    </div>

    <div class="collection-grid">
      <div v-for="item in collections" :key="item.id" class="collection-card card slide-up" @click="viewResource(item.resource)">
        <div class="card-status">
          <span class="type-tag">{{ item.resource?.type_name || item.resource?.type?.name || '未分类' }}</span>
        </div>
        <div class="card-body">
          <h3 class="card-title">{{ item.resource?.title || '未知资源' }}</h3>
          <p class="card-desc">{{ item.resource?.description || '暂无描述' }}</p>
          <div class="card-meta">
            <span class="meta-item">
              <IconDownload class="meta-icon" />
              <span>{{ item.resource?.downloads ?? 0 }} 次下载</span>
            </span>
            <span class="meta-item">
              <IconClock class="meta-icon" />
              <span>{{ formatDateTime(item.collect_date) }}</span>
            </span>
          </div>
        </div>
        <div class="card-footer" @click.stop>
          <button @click="downloadResource(item.resource)" class="btn btn-primary btn-sm">
            <IconDownload class="btn-icon" />
            <span>下载</span>
          </button>
          <button @click="uncollect(item)" class="btn btn-outline btn-sm">
            <IconClose class="btn-icon" />
            <span>取消收藏</span>
          </button>
        </div>
      </div>
    </div>

    <div v-if="collections.length === 0" class="empty-state card full-width fade-in">
      <IconBook class="empty-icon" />
      <p class="empty-title">还没有收藏任何资源</p>
      <p class="empty-sub">去资源大厅收藏感兴趣的内容吧</p>
      <button @click="goToCourses" class="btn btn-primary mt-4">
        <IconBook class="btn-icon" />
        <span>浏览资源</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { formatDateTime } from '../../utils/timeFormat'
import { useToast } from '../../composables/useToast'
import { IconCollection, IconDownload, IconClock, IconClose, IconBook } from '../icons'

const toast = useToast()
const router = useRouter()
const collections = ref<any[]>([])

const fetchCollections = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('http://127.0.0.1:8000/api/courses/collections/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    collections.value = res.data
  } catch (e) {
    console.error('获取收藏列表失败', e)
  }
}

const uncollect = async (item: any) => {
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`http://127.0.0.1:8000/api/courses/uncollect/${item.id}/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    collections.value = collections.value.filter(c => c.id !== item.id)
    toast.success('已取消收藏！')
  } catch (e: any) {
    console.error('取消收藏失败:', e)
    const msg = e.response?.data?.detail || e.response?.data?.error || '取消失败，请稍后重试'
    toast.error(msg)
  }
}

const viewResource = (resource: any) => {
  if (!resource) return
  router.push(`/student/courses/${resource.id}`)
}

const downloadResource = async (resource: any) => {
  if (!resource) return
  try {
    if (!resource.file_url) {
      toast.warning('该资源暂无下载链接')
      return
    }

    const token = localStorage.getItem('token')
    await axios.post(`http://127.0.0.1:8000/api/courses/${resource.id}/download/`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    })
    const link = document.createElement('a')
    link.href = resource.file_url
    link.target = '_blank'
    link.download = resource.title || 'download'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    toast.success('下载已开始！')
  } catch (e: any) {
    console.error('下载失败:', e)
    const msg = e.response?.data?.detail || e.response?.data?.error || '下载失败，请稍后重试'
    toast.error(msg)
  }
}

const goToCourses = () => {
  router.push('/student/courses')
}

onMounted(fetchCollections)
</script>

<style scoped>
.page-container { 
  padding: var(--spacing-lg); 
  max-width: 1200px; 
  margin: 0 auto; 
  min-height: 100vh;
}

.page-header {
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-md);
  border-bottom: 2px solid var(--border-color);
}

.header-content h2 {
  margin: 0 0 var(--spacing-xs); 
  font-size: var(--font-size-2xl); 
  font-weight: var(--font-weight-bold); 
  color: var(--text-primary); 
  display: flex; 
  align-items: center;
  gap: 12px;
  font-family: var(--font-sf);
}

.subtitle {
  color: var(--text-secondary); 
  font-size: var(--font-size-sm);
  margin: 0;
}

.header-icon { 
  width: 28px; 
  height: 28px; 
  color: var(--primary-color); 
}

.collection-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
  margin-bottom: var(--spacing-xl);
}

.card {
  background: var(--bg-primary);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--border-light);
  position: relative;
  overflow: hidden;
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-light);
}

.card-status {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 10;
}

.type-tag {
  background: rgba(13, 148, 136, 0.1);
  color: var(--primary-color);
  padding: 6px 14px;
  border-radius: var(--border-radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  backdrop-filter: blur(8px);
}

.card-body {
  padding: 24px;
  flex: 1;
  margin-top: 10px;
}

.card-title {
  margin: 0 0 12px;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-desc {
  margin: 0 0 16px;
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  padding-top: 16px;
  border-top: 1px solid var(--border-light);
  margin-bottom: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
}

.meta-icon { 
  width: 14px; 
  height: 14px; 
  color: var(--text-tertiary);
}

.card-footer {
  padding: 16px 24px;
  border-top: 1px solid var(--border-light);
  display: flex;
  gap: 12px;
  background: var(--bg-secondary);
}

.btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: var(--border-radius-md);
  font-weight: var(--font-weight-medium);
  font-size: var(--font-size-sm);
  cursor: pointer;
  border: none;
  transition: all var(--transition-fast);
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
  opacity: 0;
  transition: opacity 0.3s;
}

.btn:hover::before {
  opacity: 1;
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(13, 148, 136, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(13, 148, 136, 0.4);
}

.btn-outline {
  background: transparent;
  border: 2px solid var(--border-color);
  color: var(--text-secondary);
}

.btn-outline:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
  background: rgba(13, 148, 136, 0.05);
}

.btn-sm {
  padding: 8px 12px;
  font-size: var(--font-size-xs);
}

.btn-icon {
  width: 16px;
  height: 16px;
}

.full-width {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.empty-state {
  padding: 80px 40px;
  text-align: center;
  color: var(--text-tertiary);
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin-bottom: var(--spacing-md);
  color: var(--text-tertiary);
  opacity: 0.6;
}

.empty-title {
  font-size: var(--font-size-lg);
  color: var(--text-secondary);
  margin: 0 0 var(--spacing-xs);
  font-weight: var(--font-weight-medium);
}

.empty-sub {
  font-size: var(--font-size-sm);
  margin: 0 0 var(--spacing-md);
  color: var(--text-tertiary);
}

.mt-4 {
  margin-top: 16px;
}

.fade-in {
  animation: fadeIn var(--transition-normal);
}

.slide-up {
  animation: slideUp var(--transition-normal);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .collection-grid {
    grid-template-columns: 1fr;
  }
  
  .page-header {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }
  
  .card-footer {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}
</style>
