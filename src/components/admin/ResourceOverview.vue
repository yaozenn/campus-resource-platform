<template>
  <div class="page-container">
    <div class="page-header">
      <button @click="goBack" class="btn-back">
        <IconArrowLeft class="btn-icon" />
        返回数据分析
      </button>
      <h2>
        <IconBookOpen class="header-icon" />
        资源总览
      </h2>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-summary">
      <div class="summary-card">
        <div class="summary-icon"><IconBookOpen class="icon-svg" /></div>
        <div class="summary-value">{{ totalResources }}</div>
        <div class="summary-label">总资源数</div>
      </div>
      <div class="summary-card">
        <div class="summary-icon"><IconCheck class="icon-svg" /></div>
        <div class="summary-value">{{ activeResources }}</div>
        <div class="summary-label">已发布</div>
      </div>
      <div class="summary-card">
        <div class="summary-icon"><IconClock class="icon-svg" /></div>
        <div class="summary-value">{{ pendingResources }}</div>
        <div class="summary-label">待审核</div>
      </div>
      <div class="summary-card">
        <div class="summary-icon"><IconClose class="icon-svg" /></div>
        <div class="summary-value">{{ rejectedResources }}</div>
        <div class="summary-label">已拒绝</div>
      </div>
      <div class="summary-card">
        <div class="summary-icon"><IconDownload class="icon-svg" /></div>
        <div class="summary-value">{{ totalDownloads }}</div>
        <div class="summary-label">总下载次数</div>
      </div>
      <div class="summary-card">
        <div class="summary-icon"><IconMessage class="icon-svg" /></div>
        <div class="summary-value">{{ totalComments }}</div>
        <div class="summary-label">总评论数</div>
      </div>
    </div>

    <!-- 资源类型分布 -->
    <div class="type-distribution">
      <h3>资源类型分布</h3>
      <div class="type-grid">
        <div v-for="(count, type) in resourceTypeDistribution" :key="type" class="type-card">
          <div class="type-value">{{ count }}</div>
          <div class="type-label">{{ type }}</div>
        </div>
      </div>
    </div>

    <!-- 资源列表 -->
    <div class="resource-section">
      <h3>资源列表</h3>
      <div class="filter-bar">
        <input v-model="searchText" placeholder="搜索资源标题..." class="search-input" />
        <select v-model="filterStatus" class="filter-select">
          <option value="">全部状态</option>
          <option value="active">已发布</option>
          <option value="pending">待审核</option>
          <option value="rejected">已拒绝</option>
        </select>
      </div>
      
      <div class="resource-list">
        <div v-for="resource in filteredResources" :key="resource.id" class="resource-card">
          <div class="resource-title">{{ resource.title }}</div>
          <div class="resource-meta">
            <span class="type-tag">{{ resource.type_name || '未分类' }}</span>
            <span><IconDiamond class="meta-icon-svg" /> {{ resource.points_required }} 积分</span>
            <span><IconDownload class="meta-icon-svg" /> {{ resource.downloads }} 次下载</span>
            <span :class="['status-tag', resource.status]">{{ getStatusText(resource.status) }}</span>
          </div>
          <div class="resource-uploader">
            上传人：{{ resource.uploader?.name || resource.uploader?.username || '未知' }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { IconBookOpen, IconCheck, IconClock, IconClose, IconDownload, IconMessage, IconArrowLeft, IconDiamond } from '@/components/icons'

const router = useRouter()
const resources = ref<any[]>([])
const searchText = ref('')
const filterStatus = ref('')

const totalResources = computed(() => resources.value.length)
const activeResources = computed(() => resources.value.filter(r => r.status === 'active').length)
const pendingResources = computed(() => resources.value.filter(r => r.status === 'pending').length)
const rejectedResources = computed(() => resources.value.filter(r => r.status === 'rejected').length)
const totalDownloads = computed(() => resources.value.reduce((sum, r) => sum + (r.downloads || 0), 0))
const totalComments = computed(() => resources.value.reduce((sum, r) => sum + (r.comment_count || 0), 0))
const resourceTypeDistribution = computed(() => {
  const distribution: any = {}
  resources.value.forEach(r => {
    const type = r.type_name || '未分类'
    distribution[type] = (distribution[type] || 0) + 1
  })
  return distribution
})

const filteredResources = computed(() => {
  return resources.value.filter(resource => {
    const matchSearch = searchText.value === '' || 
                       resource.title.toLowerCase().includes(searchText.value.toLowerCase())
    const matchStatus = filterStatus.value === '' || resource.status === filterStatus.value
    return matchSearch && matchStatus
  })
})

const getStatusText = (status: string) => {
  const map: any = { active: '已发布', pending: '待审核', rejected: '已拒绝', approved: '已通过' }
  return map[status] || status
}

const fetchResources = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/courses/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    resources.value = response.data
  } catch (error) {
    console.error('获取资源列表失败', error)
  }
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  fetchResources()
})
</script>

<style scoped>
.page-container { padding: var(--spacing-lg); }

.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: var(--spacing-lg);
}

.btn-back {
  padding: 10px 20px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  cursor: pointer;
  font-size: var(--font-size-base);
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all var(--transition-fast);
}

.btn-back:hover {
  background: var(--bg-tertiary);
  border-color: var(--primary-color);
}

.btn-icon { width: 16px; height: 16px; }

.page-header h2 {
  margin: 0;
  color: var(--text-primary);
  font-size: var(--h2-font-size);
  font-weight: var(--h2-font-weight);
  display: flex;
  align-items: center;
}

.header-icon { width: 28px; height: 28px; color: var(--primary-color); margin-right: 10px; }

.stats-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.summary-card {
  background: var(--bg-primary);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  text-align: center;
  transition: box-shadow var(--transition-normal);
}

.summary-card:hover { box-shadow: var(--shadow-md); }

.summary-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto var(--spacing-sm);
  background: rgba(13, 148, 136, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-svg { width: 24px; height: 24px; color: var(--primary-color); }

.summary-value {
  font-size: 32px;
  font-weight: var(--font-weight-bold);
  color: var(--primary-color);
  margin-bottom: 8px;
}

.summary-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.resource-section h3 {
  margin-bottom: var(--spacing-md);
  color: var(--text-primary);
  font-size: var(--h4-font-size);
  font-weight: var(--h4-font-weight);
}

.filter-bar {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.search-input, .filter-select {
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-base);
  background: var(--bg-primary);
  transition: border-color var(--transition-fast);
}

.search-input:focus, .filter-select:focus {
  outline: none;
  border-color: var(--primary-color);
}

.search-input {
  flex: 1;
}

.filter-select {
  min-width: 150px;
}

.resource-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.resource-card {
  background: var(--bg-primary);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  transition: box-shadow var(--transition-normal);
}

.resource-card:hover { box-shadow: var(--shadow-md); }

.resource-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.resource-meta {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-bottom: var(--spacing-sm);
}

.resource-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.meta-icon-svg { width: 14px; height: 14px; }

.type-tag {
  padding: 4px 12px;
  background: var(--bg-secondary);
  border-radius: var(--border-radius-full);
  font-size: var(--font-size-xs);
}

.status-tag {
  padding: 4px 12px;
  border-radius: var(--border-radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
}

.status-tag.active {
  background: rgba(16, 185, 129, 0.1);
  color: var(--success-color);
}

.status-tag.pending {
  background: rgba(245, 158, 11, 0.1);
  color: var(--warning-color);
}

.status-tag.rejected {
  background: rgba(239, 68, 68, 0.1);
  color: var(--danger-color);
}

.resource-uploader {
  font-size: var(--font-size-sm);
  color: var(--text-tertiary);
}

.type-distribution {
  margin-bottom: var(--spacing-lg);
}

.type-distribution h3 {
  margin-bottom: var(--spacing-md);
  color: var(--text-primary);
  font-size: var(--h4-font-size);
  font-weight: var(--h4-font-weight);
}

.type-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--spacing-md);
}

.type-card {
  background: var(--bg-primary);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  text-align: center;
  transition: box-shadow var(--transition-normal);
}

.type-card:hover { box-shadow: var(--shadow-md); }

.type-value {
  font-size: 24px;
  font-weight: var(--font-weight-bold);
  color: var(--primary-color);
  margin-bottom: 8px;
}

.type-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}
</style>
