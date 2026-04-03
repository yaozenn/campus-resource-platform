<template>
  <div class="page-container">
    <div class="page-header">
      <button v-if="showDetailView" @click="backToList" class="btn-back">
        <IconArrowLeft class="btn-icon" />
        返回列表
      </button>
      <button v-else @click="goBack" class="btn-back">
        <IconArrowLeft class="btn-icon" />
        返回数据分析
      </button>
      <h2>
        <IconBookOpen class="header-icon" />
        资源管理
      </h2>
    </div>

    <div v-if="!showDetailView" class="stats-summary">
      <div class="summary-card primary">
        <div class="summary-icon"><IconBookOpen class="icon-svg" /></div>
        <div class="summary-value">{{ totalResources }}</div>
        <div class="summary-label">总资源数</div>
      </div>
      <div class="summary-card success">
        <div class="summary-icon"><IconCheck class="icon-svg" /></div>
        <div class="summary-value">{{ activeResources }}</div>
        <div class="summary-label">已发布</div>
      </div>
      <div class="summary-card warning">
        <div class="summary-icon"><IconClock class="icon-svg" /></div>
        <div class="summary-value">{{ pendingResources }}</div>
        <div class="summary-label">待审核</div>
      </div>
      <div class="summary-card danger">
        <div class="summary-icon"><IconClose class="icon-svg" /></div>
        <div class="summary-value">{{ rejectedResources }}</div>
        <div class="summary-label">已拒绝</div>
      </div>
      <div class="summary-card">
        <div class="summary-icon"><IconDownload class="icon-svg" /></div>
        <div class="summary-value">{{ totalDownloads }}</div>
        <div class="summary-label">总下载次数</div>
      </div>
    </div>

    <div v-if="!showDetailView" class="content-section">
      <div class="section-header">
        <h3>资源分类入口</h3>
      </div>
      <div class="category-cards">
        <div v-for="cat in mainCategories" :key="cat.id" class="category-card" @click="enterCategory(cat.id)">
          <div class="category-cover" :class="cat.coverClass">
            <component :is="cat.icon" class="category-icon" />
          </div>
          <div class="category-body">
            <h3>{{ cat.title }}</h3>
            <p>{{ cat.desc }}</p>
            <div class="category-count">{{ getCategoryCount(cat.id) }} 个资源</div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showDetailView" class="detail-section">
      <div class="detail-header">
        <h3>{{ currentCategoryTitle }}</h3>
        <div class="filter-bar">
          <input v-model="searchText" placeholder="搜索资源标题..." class="search-input" />
          <select v-model="filterStatus" class="filter-select">
            <option value="">全部状态</option>
            <option value="active">已发布</option>
            <option value="pending">待审核</option>
            <option value="rejected">已拒绝</option>
          </select>
        </div>
      </div>

      <div class="resource-grid">
        <div v-for="resource in filteredResources" :key="resource.id" class="resource-card" @click="viewResourceDetail(resource)">
          <div class="resource-cover" :class="getCoverClass(currentCategoryTitle)">
            <div class="cover-overlay"></div>
            <div class="cover-content">
              <component :is="getIcon(currentCategoryTitle)" class="cover-icon" />
              <span class="cover-type">{{ resource.type_name || '未分类' }}</span>
            </div>
            <div v-if="resource.status === 'pending'" class="status-badge pending">待审核</div>
            <div v-else-if="resource.status === 'rejected'" class="status-badge rejected">已拒绝</div>
          </div>

          <div class="resource-body">
            <h4 class="resource-title">{{ resource.title }}</h4>
            <p class="resource-desc">{{ resource.description || '暂无描述' }}</p>
            <div class="resource-meta">
              <div class="meta-item">
                <IconUser class="meta-icon" />
                <span class="uploader-link" @click.stop="viewUploader(resource.uploader_info || resource.uploader)">
                  {{ resource.uploader_name || resource.uploader_username || resource.uploader_info?.name || resource.uploader_info?.username || '未知' }}
                </span>
              </div>
              <div class="meta-item">
                <IconDownload class="meta-icon" />
                <span>{{ resource.downloads }} 次</span>
              </div>
              <div class="meta-item">
                <IconDiamond class="meta-icon" />
                <span>{{ resource.points_required }} 积分</span>
              </div>
              <div class="meta-item">
                <IconCalendar class="meta-icon" />
                <span>{{ formatDate(resource.upload_date) }}</span>
              </div>
            </div>
          </div>

          <div class="resource-actions" @click.stop>
            <button v-if="resource.status === 'pending'" @click="approveResource(resource)" class="action-btn approve">
              <IconCheck class="icon-small" /> 通过
            </button>
            <button v-if="resource.status === 'pending'" @click="rejectResource(resource)" class="action-btn reject">
              <IconClose class="icon-small" /> 拒绝
            </button>
            <button @click="deleteResource(resource)" class="action-btn delete">
              <IconTrash class="icon-small" /> 删除
            </button>
          </div>
        </div>

        <div v-if="filteredResources.length === 0" class="empty-state">
          <IconBookOpen class="empty-icon" />
          <p>暂无资源数据</p>
        </div>
      </div>
    </div>

    <div v-if="showUploaderDialog" class="dialog-overlay" @click="showUploaderDialog = false">
      <div class="dialog" @click.stop>
        <div class="dialog-header">
          <h3>上传者信息</h3>
          <button @click="showUploaderDialog = false" class="dialog-close">✕</button>
        </div>
        <div class="dialog-body" v-if="currentUploader">
          <div class="uploader-avatar">
            <IconUser class="avatar-icon" />
          </div>
          <div class="uploader-info">
            <div class="info-row">
              <span class="info-label">用户名</span>
              <span class="info-value">{{ currentUploader.username }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">姓名</span>
              <span class="info-value">{{ currentUploader.name || '-' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">角色</span>
              <span class="info-value">{{ getRoleText(currentUploader.role) }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">邮箱</span>
              <span class="info-value">{{ currentUploader.email || '-' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">手机</span>
              <span class="info-value">{{ currentUploader.phone || '-' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showResourceDialog" class="dialog-overlay" @click="showResourceDialog = false">
      <div class="dialog resource-detail-dialog" @click.stop>
        <div class="dialog-header">
          <h3>资源详情</h3>
          <button @click="showResourceDialog = false" class="dialog-close">✕</button>
        </div>
        <div class="dialog-body" v-if="currentResource">
          <div class="detail-cover" :class="getCoverClass(currentCategoryTitle)">
            <component :is="getIcon(currentCategoryTitle)" class="detail-icon" />
          </div>
          <div class="detail-info">
            <h4 class="detail-title">{{ currentResource.title }}</h4>
            <div class="detail-meta">
              <span :class="['status-badge', currentResource.status]">{{ getStatusText(currentResource.status) }}</span>
              <span class="meta-divider">|</span>
              <span>{{ currentResource.type_name || '未分类' }}</span>
            </div>
            <div class="detail-section-item">
              <span class="section-label">描述</span>
              <p class="section-content">{{ currentResource.description || '暂无描述' }}</p>
            </div>
            <div class="detail-stats">
              <div class="stat-item">
                <IconDownload class="stat-icon" />
                <span class="stat-value">{{ currentResource.downloads }}</span>
                <span class="stat-label">下载次数</span>
              </div>
              <div class="stat-item">
                <IconDiamond class="stat-icon" />
                <span class="stat-value">{{ currentResource.points_required }}</span>
                <span class="stat-label">所需积分</span>
              </div>
              <div class="stat-item">
                <IconCalendar class="stat-icon" />
                <span class="stat-value">{{ formatDate(currentResource.upload_date) }}</span>
                <span class="stat-label">上传时间</span>
              </div>
            </div>
            <div class="detail-section-item">
              <span class="section-label">上传者</span>
              <div class="uploader-card" @click="viewUploader(currentResource.uploader_info || currentResource.uploader)">
                <IconUser class="uploader-icon" />
                <div class="uploader-text">
                  <span class="uploader-name">{{ currentResource.uploader_name || currentResource.uploader_username || currentResource.uploader_info?.name || currentResource.uploader_info?.username || '未知' }}</span>
                  <span class="uploader-role">{{ getRoleText(currentResource.uploader_info?.role || currentResource.uploader?.role) }}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="dialog-footer">
            <button v-if="currentResource.status === 'pending'" @click="approveResource(currentResource); showResourceDialog = false" class="btn-approve">
              <IconCheck class="icon-small" /> 通过审核
            </button>
            <button v-if="currentResource.status === 'pending'" @click="rejectResource(currentResource); showResourceDialog = false" class="btn-reject">
              <IconClose class="icon-small" /> 拒绝
            </button>
            <button @click="deleteResource(currentResource); showResourceDialog = false" class="btn-delete">
              <IconTrash class="icon-small" /> 删除资源
            </button>
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
import { 
  IconBookOpen, IconCheck, IconClock, IconClose, 
  IconDownload, IconArrowLeft, IconDiamond, IconTrash,
  IconUser, IconCalendar, IconVideo, IconDocument
} from '@/components/icons'

const router = useRouter()
const resources = ref<any[]>([])
const searchText = ref('')
const filterStatus = ref('')
const showDetailView = ref(false)
const currentCategory = ref('')
const showUploaderDialog = ref(false)
const currentUploader = ref<any>(null)
const showResourceDialog = ref(false)
const currentResource = ref<any>(null)

const mainCategories = [
  { id: '课程资源', title: '课程资源', desc: '课件、讲义、习题等学习资料', coverClass: 'cover-courseware', icon: IconBookOpen },
  { id: '网络资源', title: '网络资源', desc: '在线课程、视频教程等', coverClass: 'cover-video', icon: IconVideo },
  { id: '书籍资源', title: '书籍资源', desc: '电子书、参考书籍等', coverClass: 'cover-ebook', icon: IconDocument }
]

const currentCategoryTitle = computed(() => currentCategory.value)

const totalResources = computed(() => resources.value.length)
const activeResources = computed(() => resources.value.filter(r => r.status === 'active').length)
const pendingResources = computed(() => resources.value.filter(r => r.status === 'pending').length)
const rejectedResources = computed(() => resources.value.filter(r => r.status === 'rejected').length)
const totalDownloads = computed(() => resources.value.reduce((sum, r) => sum + (r.downloads || 0), 0))

const getCategoryCount = (catId: string) => {
  return resources.value.filter(r => r.type_description === catId).length
}

const filteredResources = computed(() => {
  return resources.value.filter(resource => {
    const matchCategory = resource.type_description === currentCategory.value
    const matchSearch = searchText.value === '' || 
                       resource.title.toLowerCase().includes(searchText.value.toLowerCase())
    const matchStatus = filterStatus.value === '' || resource.status === filterStatus.value
    return matchCategory && matchSearch && matchStatus
  })
})

const getCoverClass = (cat: string) => {
  if (cat === '课程资源') return 'cover-courseware'
  if (cat === '网络资源') return 'cover-video'
  if (cat === '书籍资源') return 'cover-ebook'
  return 'cover-default'
}

const getIcon = (cat: string) => {
  if (cat === '课程资源') return IconBookOpen
  if (cat === '网络资源') return IconVideo
  if (cat === '书籍资源') return IconDocument
  return IconBookOpen
}

const getStatusText = (status: string) => {
  const map: any = { active: '已发布', pending: '待审核', rejected: '已拒绝', approved: '已通过' }
  return map[status] || status
}

const getRoleText = (role: string) => {
  const map: any = { student: '学生', teacher: '教师', admin: '管理员' }
  return map[role] || role || '未知'
}

const formatDate = (d: string) => {
  if (!d) return '-'
  return new Date(d).toLocaleDateString('zh-CN')
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

const enterCategory = (catId: string) => {
  currentCategory.value = catId
  showDetailView.value = true
  searchText.value = ''
  filterStatus.value = ''
}

const backToList = () => {
  showDetailView.value = false
  currentCategory.value = ''
}

const viewUploader = (uploader: any) => {
  currentUploader.value = uploader
  showUploaderDialog.value = true
}

const viewResourceDetail = (resource: any) => {
  currentResource.value = resource
  showResourceDialog.value = true
}

const approveResource = async (resource: any) => {
  if (!confirm(`确定要通过资源「${resource.title}」的审核吗？`)) return
  try {
    const token = localStorage.getItem('token')
    await axios.put(`http://127.0.0.1:8000/api/courses/${resource.id}/status/`, 
      { status: 'active' },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    resource.status = 'active'
    alert('审核通过！')
  } catch (error: any) {
    console.error('审核失败', error)
    alert(error.response?.data?.detail || '操作失败，请稍后重试')
  }
}

const rejectResource = async (resource: any) => {
  if (!confirm(`确定要拒绝资源「${resource.title}」吗？`)) return
  try {
    const token = localStorage.getItem('token')
    await axios.put(`http://127.0.0.1:8000/api/courses/${resource.id}/status/`, 
      { status: 'rejected' },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    resource.status = 'rejected'
    alert('已拒绝该资源')
  } catch (error: any) {
    console.error('拒绝失败', error)
    alert(error.response?.data?.detail || '操作失败，请稍后重试')
  }
}

const deleteResource = async (resource: any) => {
  if (!confirm(`确定要删除资源「${resource.title}」吗？此操作不可恢复！`)) return
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`http://127.0.0.1:8000/api/courses/${resource.id}/`, 
      { headers: { Authorization: `Bearer ${token}` } }
    )
    resources.value = resources.value.filter(r => r.id !== resource.id)
    alert('删除成功！')
  } catch (error: any) {
    console.error('删除失败', error)
    alert(error.response?.data?.detail || '删除失败，请稍后重试')
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
  grid-template-columns: repeat(5, 1fr);
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.summary-card {
  background: var(--bg-primary);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  text-align: center;
  transition: all var(--transition-normal);
  border: 1px solid var(--border-light);
}

.summary-card:hover { 
  transform: translateY(-2px);
  box-shadow: var(--shadow-md); 
}

.summary-card.primary { border-left: 4px solid var(--primary-color); }
.summary-card.success { border-left: 4px solid var(--success-color); }
.summary-card.warning { border-left: 4px solid var(--warning-color); }
.summary-card.danger { border-left: 4px solid var(--danger-color); }

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
  color: var(--text-primary);
  margin-bottom: 8px;
}

.summary-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.content-section {
  background: var(--bg-primary);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
}

.section-header h3 {
  margin: 0 0 var(--spacing-lg);
  color: var(--text-primary);
  font-size: var(--h4-font-size);
  font-weight: var(--h4-font-weight);
}

.category-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

.category-card {
  background: var(--bg-secondary);
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid var(--border-light);
}

.category-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-color);
}

.category-cover {
  height: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cover-courseware { background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%); }
.cover-video { background: linear-gradient(135deg, #0ea5e9 0%, #38bdf8 100%); }
.cover-ebook { background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%); }

.category-icon { width: 56px; height: 56px; color: white; opacity: 0.9; }

.category-body { padding: 20px; text-align: center; }
.category-body h3 { margin: 0 0 8px; font-size: 18px; color: var(--text-primary); }
.category-body p { margin: 0 0 12px; font-size: 13px; color: var(--text-secondary); }
.category-count {
  display: inline-block;
  padding: 6px 16px;
  background: var(--primary-soft);
  color: var(--primary-dark);
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.detail-section {
  background: var(--bg-primary);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.detail-header h3 {
  margin: 0;
  color: var(--text-primary);
  font-size: var(--h4-font-size);
}

.filter-bar {
  display: flex;
  gap: var(--spacing-md);
}

.search-input, .filter-select {
  padding: 10px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-sm);
  background: var(--bg-secondary);
  transition: all var(--transition-fast);
}

.search-input:focus, .filter-select:focus {
  outline: none;
  border-color: var(--primary-color);
  background: var(--bg-primary);
}

.search-input { width: 240px; }
.filter-select { min-width: 120px; }

.resource-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

.resource-card {
  background: var(--bg-secondary);
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid var(--border-light);
}

.resource-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-color);
}

.resource-cover {
  position: relative;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cover-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, transparent, rgba(0,0,0,0.3));
}

.cover-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: white;
}

.cover-icon { width: 40px; height: 40px; }
.cover-type {
  font-size: 12px;
  padding: 4px 12px;
  background: rgba(255,255,255,0.2);
  border-radius: 20px;
}

.resource-body { padding: 16px; }
.resource-title {
  margin: 0 0 8px;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.resource-desc {
  margin: 0 0 12px;
  font-size: 13px;
  color: var(--text-secondary);
  height: 40px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
.resource-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-secondary);
}
.meta-icon { width: 14px; height: 14px; }
.uploader-link {
  color: var(--primary-color);
  cursor: pointer;
}
.uploader-link:hover { text-decoration: underline; }

.resource-actions {
  display: flex;
  gap: 8px;
  padding: 0 16px 16px;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 8px 12px;
  border: none;
  border-radius: var(--border-radius-md);
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: all var(--transition-fast);
  flex: 1;
}

.action-btn.approve {
  background: rgba(16, 185, 129, 0.1);
  color: var(--success-color);
}
.action-btn.approve:hover {
  background: var(--success-color);
  color: white;
}

.action-btn.reject {
  background: rgba(239, 68, 68, 0.1);
  color: var(--danger-color);
}
.action-btn.reject:hover {
  background: var(--danger-color);
  color: white;
}

.action-btn.delete {
  background: rgba(156, 163, 175, 0.1);
  color: var(--text-secondary);
}
.action-btn.delete:hover {
  background: var(--danger-color);
  color: white;
}

.icon-small { width: 14px; height: 14px; }

.status-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  z-index: 2;
}

.status-badge.active { background: rgba(16, 185, 129, 0.9); color: white; }
.status-badge.pending { background: rgba(245, 158, 11, 0.9); color: white; }
.status-badge.rejected { background: rgba(239, 68, 68, 0.9); color: white; }

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px 20px;
  color: var(--text-tertiary);
}

.empty-icon { width: 48px; height: 48px; margin-bottom: 16px; opacity: 0.5; }

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog {
  background: var(--bg-primary);
  border-radius: var(--border-radius-lg);
  width: 420px;
  max-width: 90%;
  box-shadow: var(--shadow-xl);
}

.resource-detail-dialog {
  width: 560px;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-light);
}

.dialog-header h3 {
  margin: 0;
  font-size: 18px;
  color: var(--text-primary);
}

.dialog-close {
  background: none;
  border: none;
  font-size: 20px;
  color: var(--text-tertiary);
  cursor: pointer;
}

.dialog-body { padding: 24px; }

.uploader-avatar {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  background: var(--primary-soft);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-icon { width: 40px; height: 40px; color: var(--primary-color); }

.uploader-info { display: flex; flex-direction: column; gap: 12px; }
.info-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border-light); }
.info-label { color: var(--text-secondary); font-size: 14px; }
.info-value { color: var(--text-primary); font-size: 14px; font-weight: 500; }

.detail-cover {
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-md);
  margin-bottom: 20px;
}

.detail-icon { width: 48px; height: 48px; color: white; }

.detail-info { display: flex; flex-direction: column; gap: 16px; }
.detail-title { margin: 0; font-size: 20px; color: var(--text-primary); }
.detail-meta { display: flex; align-items: center; gap: 8px; font-size: 13px; color: var(--text-secondary); }
.meta-divider { color: var(--border-color); }

.detail-section-item { display: flex; flex-direction: column; gap: 8px; }
.section-label { font-size: 13px; color: var(--text-secondary); font-weight: 500; }
.section-content { margin: 0; font-size: 14px; color: var(--text-primary); line-height: 1.6; }

.detail-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  padding: 16px;
  background: var(--bg-secondary);
  border-radius: var(--border-radius-md);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.stat-icon { width: 20px; height: 20px; color: var(--primary-color); }
.stat-value { font-size: 18px; font-weight: 600; color: var(--text-primary); }
.stat-label { font-size: 12px; color: var(--text-secondary); }

.uploader-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--bg-secondary);
  border-radius: var(--border-radius-md);
  cursor: pointer;
  transition: all 0.2s;
}

.uploader-card:hover { background: var(--bg-tertiary); }

.uploader-icon { width: 32px; height: 32px; color: var(--primary-color); }
.uploader-text { display: flex; flex-direction: column; gap: 2px; }
.uploader-name { font-size: 14px; font-weight: 500; color: var(--text-primary); }
.uploader-role { font-size: 12px; color: var(--text-secondary); }

.dialog-footer {
  display: flex;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid var(--border-light);
}

.btn-approve, .btn-reject, .btn-delete {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 16px;
  border: none;
  border-radius: var(--border-radius-md);
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-approve { background: var(--success-color); color: white; }
.btn-approve:hover { opacity: 0.9; }

.btn-reject { background: var(--warning-color); color: white; }
.btn-reject:hover { opacity: 0.9; }

.btn-delete { background: var(--danger-color); color: white; }
.btn-delete:hover { opacity: 0.9; }
</style>
