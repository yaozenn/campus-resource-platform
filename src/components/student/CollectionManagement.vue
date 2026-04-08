<template>
  <div class="page-container">
    <h2>
      <IconCollection class="header-icon" />
      收藏管理
    </h2>

    <div v-if="collections.length > 0" class="collection-grid">
      <div v-for="item in collections" :key="item.id" class="collection-card" @click="viewResource(item.resource)">
        <div class="card-top">
          <span class="type-tag">{{ item.resource?.type_name || item.resource?.type?.name || '未分类' }}</span>
        </div>
        <h3 class="card-title">{{ item.resource?.title || '未知资源' }}</h3>
        <p class="card-desc">{{ item.resource?.description || '暂无描述' }}</p>
        <div class="card-meta">
          <span><IconDownload class="meta-icon" /> {{ item.resource?.downloads ?? 0 }} 次下载</span>
          <span><IconClock class="meta-icon" /> {{ formatDateTime(item.collect_date) }}</span>
        </div>
        <div class="card-actions" @click.stop>
          <button @click="downloadResource(item.resource)" class="btn-download">
            <IconDownload class="btn-icon" /> 下载
          </button>
          <button @click="uncollect(item)" class="btn-uncollect">
            <IconClose class="btn-icon" /> 取消收藏
          </button>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <IconBook class="empty-icon-svg" />
      <p class="empty-title">还没有收藏任何资源</p>
      <p class="empty-sub">去资源浏览页面收藏感兴趣的内容吧</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { formatDateTime } from '../../utils/timeFormat'
import { useToast } from '../../composables/useToast'
import { IconCollection, IconDownload, IconClock, IconClose, IconBook } from '@/components/icons'

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

onMounted(fetchCollections)
</script>

<style scoped>
.page-container { padding: var(--spacing-lg); }
.page-container h2 { margin: 0 0 var(--spacing-lg); font-size: var(--h2-font-size); font-weight: var(--h2-font-weight); color: var(--text-primary); display: flex; align-items: center; }
.header-icon { width: 28px; height: 28px; color: var(--primary-color); margin-right: 10px; }

.collection-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-md);
}

.collection-card {
  background: var(--bg-primary);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-normal);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  cursor: pointer;
}
.collection-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}

.card-top { display: flex; justify-content: space-between; align-items: center; }
.type-tag {
  background: rgba(13, 148, 136, 0.1);
  color: var(--primary-color);
  padding: 4px 12px;
  border-radius: var(--border-radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
}

.card-title {
  margin: 0;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.card-desc {
  margin: 0;
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  padding-top: var(--spacing-sm);
  border-top: 1px solid var(--border-light);
}
.card-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}
.meta-icon { width: 12px; height: 12px; }

.card-actions { display: flex; gap: var(--spacing-sm); }
.btn-download, .btn-uncollect {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 8px 0;
  border: none;
  border-radius: var(--border-radius-md);
  cursor: pointer;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-fast);
}
.btn-icon { width: 14px; height: 14px; }
.btn-download { background: var(--primary-color); color: white; }
.btn-download:hover { background: var(--primary-hover); }
.btn-uncollect { background: rgba(239, 68, 68, 0.1); color: var(--danger-color); }
.btn-uncollect:hover { background: var(--danger-color); color: white; }

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-tertiary);
}
.empty-icon-svg { width: 64px; height: 64px; margin-bottom: var(--spacing-md); color: var(--text-tertiary); }
.empty-title { font-size: var(--font-size-base); color: var(--text-secondary); margin: 0 0 var(--spacing-xs); }
.empty-sub { font-size: var(--font-size-sm); margin: 0; }
</style>
