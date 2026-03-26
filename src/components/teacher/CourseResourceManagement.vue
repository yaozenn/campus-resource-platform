<template>
  <div class="page-container">
    <!-- Hero Header -->
    <section class="hero-header">
      <div class="hero-content">
        <div class="hero-icon">
          <IconBook class="icon-svg" />
        </div>
        <div class="hero-text">
          <h1>课程资源管理</h1>
          <p>管理和分享您的教学资源，支持视频、课件、文档等多种类型</p>
        </div>
      </div>
      <div class="hero-actions">
        <button @click="showAddDialog = true" class="btn-primary">
          <IconPlus class="btn-icon" />
          <span>添加资源</span>
        </button>
        <button @click="fetchCourses" class="btn-secondary">
          <IconRefresh class="btn-icon" />
          <span>刷新</span>
        </button>
      </div>
    </section>

    <!-- Filter Section -->
    <section class="filter-section glass">
      <div class="category-tabs">
        <button
          :class="['tab-btn', resourceCategory === 'all' ? 'active' : '']"
          @click="resourceCategory = 'all'"
        >
          <IconFolder class="tab-icon" />
          <span>全部资源</span>
        </button>
        <button
          :class="['tab-btn', resourceCategory === 'online' ? 'active' : '']"
          @click="resourceCategory = 'online'"
        >
          <IconVideo class="tab-icon" />
          <span>网络课程</span>
        </button>
        <button
          :class="['tab-btn', resourceCategory === 'campus' ? 'active' : '']"
          @click="resourceCategory = 'campus'"
        >
          <IconBook class="tab-icon" />
          <span>校内课程</span>
        </button>
        <button
          :class="['tab-btn', resourceCategory === 'books' ? 'active' : '']"
          @click="resourceCategory = 'books'"
        >
          <IconDocument class="tab-icon" />
          <span>书籍资源</span>
        </button>
      </div>

      <div class="search-bar">
        <IconSearch class="search-icon" />
        <input v-model="searchText" placeholder="搜索资源标题或描述..." class="search-input" />
        <button v-if="searchText" @click="searchText = ''" class="clear-btn">
          <IconClose class="clear-icon" />
        </button>
      </div>

      <div class="filter-bar">
        <div class="filter-group">
          <label class="filter-label">
            <IconCollection class="label-icon" />
            <span>类型</span>
          </label>
          <select v-model="filterType" class="filter-select">
            <option value="">全部类型</option>
            <option v-for="t in courseTypes" :key="t.id" :value="t.id">{{ t.name }}</option>
          </select>
        </div>

        <div class="filter-group">
          <label class="filter-label">
            <IconSort class="label-icon" />
            <span>排序</span>
          </label>
          <select v-model="sortBy" class="filter-select">
            <option value="downloads">下载最多</option>
            <option value="newest">最新上传</option>
          </select>
        </div>
      </div>
    </section>

    <!-- Resource Grid -->
    <section class="resource-section">
      <div class="resource-grid" v-if="loading">
        <div v-for="i in 6" :key="i" class="resource-card skeleton">
          <div class="skeleton-cover"></div>
          <div class="skeleton-body">
            <div class="skeleton-line title"></div>
            <div class="skeleton-line meta"></div>
            <div class="skeleton-line description"></div>
          </div>
        </div>
      </div>

      <div class="resource-grid" v-else>
        <div v-for="course in filteredCourses" :key="course.id" class="resource-card">
          <div class="resource-cover" :class="getCoverClass(course.type?.name)">
            <div class="cover-overlay"></div>
            <component :is="getCoverIcon(course.type?.name)" class="cover-icon-svg" />
            <div class="status-badge" :class="course.status">{{ getStatusText(course.status) }}</div>
          </div>
          <div class="resource-body">
            <h3 class="resource-title">{{ course.title }}</h3>
            <div class="resource-meta">
              <div class="meta-tag">
                <IconCollection class="meta-icon" />
                <span>{{ course.type?.name || '未分类' }}</span>
              </div>
              <div class="meta-tag">
                <IconDownload class="meta-icon" />
                <span>{{ course.downloads }} 次下载</span>
              </div>
            </div>
            <p class="resource-description">{{ course.description || '暂无描述' }}</p>
            <div class="resource-footer">
              <span class="upload-date">
                <IconCalendar class="date-icon" />
                {{ formatTime(course.upload_date) }}
              </span>
            </div>
          </div>
          <div class="resource-actions">
            <button @click="editCourse(course)" class="btn-edit">
              <IconEdit class="action-icon" />
              <span>编辑</span>
            </button>
            <button @click="deleteCourse(course.id)" class="btn-delete">
              <IconDelete class="action-icon" />
              <span>删除</span>
            </button>
          </div>
        </div>

        <div v-if="filteredCourses.length === 0" class="empty-state">
          <IconFolder class="empty-icon" />
          <h3>暂无资源</h3>
          <p>点击"添加资源"按钮创建您的第一个教学资源</p>
        </div>
      </div>
    </section>

    <!-- Add/Edit Dialog -->
    <div v-if="showAddDialog || showEditDialog" class="dialog-overlay" @click="closeDialog">
      <div class="dialog" @click.stop>
        <div class="dialog-header">
          <h3>{{ showEditDialog ? '编辑资源' : '添加资源' }}</h3>
          <button @click="closeDialog" class="btn-close">
            <IconClose class="close-icon" />
          </button>
        </div>
        <form @submit.prevent="saveCourse" class="dialog-form">
          <div class="form-group">
            <label>资源名称</label>
            <input v-model="currentCourse.title" placeholder="请输入资源名称" required />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>资源类型</label>
              <select v-model="currentCourse.type" required>
                <option value="">请选择类型</option>
                <option v-for="type in courseTypes" :key="type.id" :value="type.id">
                  {{ type.name }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>所需积分</label>
              <input v-model.number="currentCourse.points_required" type="number" min="0" placeholder="0" />
            </div>
          </div>
          <div class="form-group">
            <label>资源描述</label>
            <textarea v-model="currentCourse.description" placeholder="请输入资源描述" rows="3"></textarea>
          </div>
          <div class="form-group">
            <label>文件地址</label>
            <input v-model="currentCourse.file_url" placeholder="请输入文件地址或上传链接" />
          </div>
          <div class="form-group">
            <label>封面图片</label>
            <input v-model="currentCourse.cover_image" placeholder="请输入封面图片地址（可选）" />
          </div>
          <div class="form-group">
            <label>可见性设置</label>
            <div class="visibility-options">
              <label class="visibility-option" :class="{ active: currentCourse.visibility === 'public' }">
                <input type="radio" v-model="currentCourse.visibility" value="public" />
                <IconGlobe class="visibility-icon" />
                <div class="visibility-content">
                  <span class="visibility-title">公开</span>
                  <span class="visibility-desc">所有学生可见</span>
                </div>
              </label>
              <label class="visibility-option" :class="{ active: currentCourse.visibility === 'students_only' }">
                <input type="radio" v-model="currentCourse.visibility" value="students_only" />
                <IconUser class="visibility-icon" />
                <div class="visibility-content">
                  <span class="visibility-title">仅我的学生</span>
                  <span class="visibility-desc">只有我指导的学生可见</span>
                </div>
              </label>
            </div>
          </div>
          <div class="dialog-actions">
            <button type="button" @click="closeDialog" class="btn-cancel">取消</button>
            <button type="submit" class="btn-submit">
              <IconCheck class="submit-icon" />
              <span>保存</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { formatTime } from '../../utils/timeFormat'
import {
  IconBook,
  IconVideo,
  IconDocument,
  IconFolder,
  IconPlus,
  IconRefresh,
  IconSearch,
  IconClose,
  IconCollection,
  IconSort,
  IconDownload,
  IconCalendar,
  IconEdit,
  IconDelete,
  IconCheck,
  IconUser,
  IconGlobe
} from '../../components/icons'

const courses = ref<any[]>([])
const courseTypes = ref<any[]>([])
const showAddDialog = ref(false)
const showEditDialog = ref(false)
const resourceCategory = ref('all')
const searchText = ref('')
const filterType = ref('')
const sortBy = ref('newest')
const loading = ref(true)
const currentCourse = ref({
  id: 0,
  title: '',
  type: '',
  description: '',
  file_url: '',
  points_required: 0,
  is_second_hand: false,
  price: 0,
  cover_image: '',
  visibility: 'public' // public: 公开, students_only: 仅我的学生可见
})

const getStatusText = (status: string) => {
  const map: any = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝',
    active: '已发布'
  }
  return map[status] || status
}

const getCoverClass = (typeName: string) => {
  const classMap: any = {
    '视频': 'cover-video',
    'MOOC': 'cover-mooc',
    '课件': 'cover-courseware',
    '作业': 'cover-homework',
    '文档': 'cover-document',
    '电子书': 'cover-ebook'
  }
  return classMap[typeName] || 'cover-default'
}

const getCoverIcon = (typeName: string) => {
  const iconMap: any = {
    '视频': IconVideo,
    'MOOC': IconBook,
    '课件': IconBook,
    '作业': IconDocument,
    '文档': IconDocument,
    '电子书': IconBook
  }
  return iconMap[typeName] || IconFolder
}

const filteredCourses = computed(() => {
  let result = courses.value.filter(course => {
    const matchesSearch = searchText.value === '' ||
                         course.title.toLowerCase().includes(searchText.value.toLowerCase()) ||
                         (course.description && course.description.toLowerCase().includes(searchText.value.toLowerCase()))
    const matchesType = filterType.value === '' || course.type === filterType.value

    let matchesCategory = true
    if (resourceCategory.value === 'online') {
      matchesCategory = course.type_name === '视频' || course.type_name === 'MOOC'
    } else if (resourceCategory.value === 'campus') {
      matchesCategory = course.type_name === '课件' || course.type_name === '作业'
    } else if (resourceCategory.value === 'books') {
      matchesCategory = course.type_name === '文档' || course.type_name === '电子书'
    }

    return matchesSearch && matchesType && matchesCategory
  })

  if (sortBy.value === 'downloads') {
    result.sort((a, b) => b.downloads - a.downloads)
  } else if (sortBy.value === 'newest') {
    result.sort((a, b) => new Date(b.upload_date).getTime() - new Date(a.upload_date).getTime())
  }

  return result
})

const fetchCourses = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/courses/teacher/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    courses.value = response.data
  } catch (error) {
    console.error('获取资源列表失败', error)
  } finally {
    loading.value = false
  }
}

const fetchCourseTypes = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/courses/types/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    courseTypes.value = response.data
  } catch (error) {
    console.error('获取资源类型失败', error)
  }
}

const editCourse = (course: any) => {
  console.log('Editing course:', course)
  currentCourse.value = {
    id: course.id,
    title: course.title,
    type: course.type?.id || course.type || '',
    description: course.description || '',
    file_url: course.file_url || '',
    points_required: course.points_required || 0,
    is_second_hand: course.is_second_hand || false,
    price: course.price || 0,
    cover_image: course.cover_image || '',
    visibility: course.visibility || 'public'
  }
  showEditDialog.value = true
}

const closeDialog = () => {
  showAddDialog.value = false
  showEditDialog.value = false
  currentCourse.value = {
    id: 0,
    title: '',
    type: '',
    description: '',
    file_url: '',
    points_required: 0,
    is_second_hand: false,
    price: 0,
    cover_image: '',
    visibility: 'public'
  }
}

const saveCourse = async () => {
  try {
    const token = localStorage.getItem('token')

    // 确保type是数字
    const typeId = parseInt(currentCourse.value.type)
    if (isNaN(typeId)) {
      alert('请选择有效的资源类型')
      return
    }

    const submitData = {
      title: currentCourse.value.title,
      type: typeId,
      description: currentCourse.value.description,
      file_url: currentCourse.value.file_url,
      points_required: currentCourse.value.points_required,
      is_second_hand: currentCourse.value.is_second_hand,
      price: currentCourse.value.price,
      cover_image: currentCourse.value.cover_image,
      visibility: currentCourse.value.visibility
    }

    console.log('Submitting data:', submitData)
    console.log('Is edit mode:', showEditDialog.value)
    console.log('Course ID:', currentCourse.value.id)

    if (showEditDialog.value) {
      const url = `http://127.0.0.1:8000/api/courses/${currentCourse.value.id}/update/`
      console.log('PUT URL:', url)
      const response = await axios.put(url, submitData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      console.log('Edit response:', response.data)
    } else {
      const response = await axios.post(
        'http://127.0.0.1:8000/api/courses/create/',
        submitData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      )
      console.log('Create response:', response.data)
    }
    closeDialog()
    fetchCourses()
    alert('保存成功')
  } catch (error: any) {
    console.error('保存失败:', error)
    console.error('Error response:', error.response)
    console.error('Error data:', error.response?.data)
    alert('保存失败：' + (error.response?.data?.message || error.response?.data?.error || error.message || '未知错误'))
  }
}

const deleteCourse = async (id: number) => {
  if (confirm('确定要删除这个课程吗？')) {
    try {
      const token = localStorage.getItem('token')
      await axios.delete(`http://127.0.0.1:8000/api/courses/${id}/delete/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      courses.value = courses.value.filter(c => c.id !== id)
      alert('删除成功')
    } catch (error) {
      alert('删除失败')
    }
  }
}

onMounted(() => {
  fetchCourses()
  fetchCourseTypes()
})
</script>

<style scoped>
.page-container {
  padding: 0;
  background: var(--bg-color);
  min-height: calc(100vh - 64px);
}

/* Hero Header */
.hero-header {
  background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%);
  padding: 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.hero-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="white" opacity="0.1"/><circle cx="80" cy="40" r="3" fill="white" opacity="0.1"/><circle cx="40" cy="80" r="2" fill="white" opacity="0.1"/></svg>');
  background-size: 200px 200px;
}

.hero-content {
  display: flex;
  align-items: center;
  gap: 24px;
  position: relative;
  z-index: 1;
}

.hero-icon {
  width: 64px;
  height: 64px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
}

.icon-svg {
  width: 36px;
  height: 36px;
  color: white;
}

.hero-text h1 {
  font-size: 32px;
  font-weight: 700;
  color: white;
  margin: 0 0 8px;
  font-family: var(--font-sf);
}

.hero-text p {
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
  font-size: 15px;
}

.hero-actions {
  display: flex;
  gap: 12px;
  position: relative;
  z-index: 1;
}

.btn-primary, .btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  border-radius: var(--border-radius-lg);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-primary {
  background: white;
  color: var(--primary-color);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  backdrop-filter: blur(10px);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.3);
}

.btn-icon {
  width: 18px;
  height: 18px;
}

/* Filter Section */
.filter-section {
  margin: -30px 40px 30px;
  padding: 24px;
  border-radius: var(--border-radius-xl);
  position: relative;
  z-index: 2;
}

.category-tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.tab-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: white;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.tab-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.tab-btn.active {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.tab-icon {
  width: 16px;
  height: 16px;
}

.search-bar {
  position: relative;
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.search-icon {
  position: absolute;
  left: 16px;
  width: 20px;
  height: 20px;
  color: var(--text-placeholder);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 14px 48px 14px 48px;
  border: 2px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  font-size: 15px;
  transition: all var(--transition-fast);
  background: white;
  color: var(--text-primary);
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 4px rgba(13, 148, 136, 0.1);
}

.clear-btn {
  position: absolute;
  right: 12px;
  width: 32px;
  height: 32px;
  border: none;
  background: var(--bg-tertiary);
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.clear-icon {
  width: 16px;
  height: 16px;
  color: var(--text-secondary);
}

.clear-btn:hover {
  background: var(--primary-color);
}

.clear-btn:hover .clear-icon {
  color: white;
}

.filter-bar {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
}

.label-icon {
  width: 18px;
  height: 18px;
}

.filter-select {
  padding: 10px 40px 10px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  min-width: 160px;
  font-size: 14px;
  color: var(--text-primary);
  background: white;
  cursor: pointer;
  transition: all var(--transition-fast);
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23909399' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
}

.filter-select:hover {
  border-color: var(--primary-light);
}

.filter-select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
}

/* Resource Section */
.resource-section {
  padding: 0 40px 40px;
}

.resource-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.resource-card {
  background: white;
  border-radius: var(--border-radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  transition: all var(--transition-normal);
  border: 1px solid var(--border-light);
}

.resource-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-xl);
}

.resource-cover {
  position: relative;
  height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.cover-video {
  background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%);
}

.cover-mooc {
  background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);
}

.cover-courseware {
  background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
}

.cover-homework {
  background: linear-gradient(135deg, #db2777 0%, #f472b6 100%);
}

.cover-document {
  background: linear-gradient(135deg, #ea580c 0%, #fb923c 100%);
}

.cover-ebook {
  background: linear-gradient(135deg, #059669 0%, #34d399 100%);
}

.cover-default {
  background: linear-gradient(135deg, #6b7280 0%, #9ca3af 100%);
}

.cover-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.3) 100%);
}

.cover-icon-svg {
  width: 48px;
  height: 48px;
  color: white;
  opacity: 0.9;
  position: relative;
  z-index: 1;
}

.status-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  backdrop-filter: blur(10px);
  z-index: 1;
}

.status-badge.pending {
  color: #f59e0b;
}

.status-badge.approved,
.status-badge.active {
  color: #10b981;
}

.status-badge.rejected {
  color: #ef4444;
}

.resource-body {
  padding: 20px;
}

.resource-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 12px;
  line-height: 1.4;
}

.resource-meta {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.meta-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: var(--bg-tertiary);
  border-radius: 20px;
  font-size: 12px;
  color: var(--text-secondary);
}

.meta-icon {
  width: 14px;
  height: 14px;
}

.resource-description {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
  margin: 0 0 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.resource-footer {
  padding-top: 16px;
  border-top: 1px solid var(--border-light);
}

.upload-date {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-tertiary);
}

.date-icon {
  width: 14px;
  height: 14px;
}

.resource-actions {
  display: flex;
  gap: 8px;
  padding: 0 20px 20px;
}

.btn-edit, .btn-delete {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.action-icon {
  width: 16px;
  height: 16px;
}

.btn-edit {
  background: white;
  color: var(--primary-color);
  border-color: var(--primary-color);
}

.btn-edit:hover {
  background: var(--primary-color);
  color: white;
}

.btn-delete {
  background: white;
  color: #ef4444;
  border-color: #fecaca;
}

.btn-delete:hover {
  background: #fef2f2;
  border-color: #ef4444;
}

/* Empty State */
.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 80px 20px;
  color: var(--text-placeholder);
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  color: var(--text-tertiary);
}

.empty-state h3 {
  font-size: 20px;
  color: var(--text-primary);
  margin: 0 0 8px;
}

.empty-state p {
  color: var(--text-secondary);
  margin: 0;
}

/* Skeleton */
.skeleton {
  pointer-events: none;
}

.skeleton-cover {
  height: 160px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
}

.skeleton-body {
  padding: 20px;
}

.skeleton-line {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
  border-radius: 4px;
  margin-bottom: 12px;
}

.skeleton-line.title {
  height: 24px;
  width: 80%;
}

.skeleton-line.meta {
  height: 16px;
  width: 60%;
}

.skeleton-line.description {
  height: 14px;
  width: 100%;
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Dialog */
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
  padding: 20px;
}

.dialog {
  background: white;
  border-radius: var(--border-radius-2xl);
  width: 100%;
  max-width: 560px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-xl);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 0;
}

.dialog-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
}

.btn-close {
  width: 36px;
  height: 36px;
  border: none;
  background: var(--bg-tertiary);
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.close-icon {
  width: 18px;
  height: 18px;
  color: var(--text-secondary);
}

.btn-close:hover {
  background: var(--bg-secondary);
}

.dialog-form {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 500;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: 14px;
  color: var(--text-primary);
  background: white;
  transition: all var(--transition-fast);
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
}

/* Visibility Options */
.visibility-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.visibility-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border: 2px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all var(--transition-fast);
  background: white;
}

.visibility-option input {
  display: none;
}

.visibility-option:hover {
  border-color: var(--primary-light);
  background: rgba(13, 148, 136, 0.05);
}

.visibility-option.active {
  border-color: var(--primary-color);
  background: rgba(13, 148, 136, 0.1);
}

.visibility-icon {
  width: 24px;
  height: 24px;
  color: var(--primary-color);
  flex-shrink: 0;
}

.visibility-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.visibility-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.visibility-desc {
  font-size: 12px;
  color: var(--text-tertiary);
}

.form-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 16px;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid var(--border-light);
}

.btn-cancel {
  padding: 12px 24px;
  border: 1px solid var(--border-color);
  background: white;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  transition: all var(--transition-fast);
}

.btn-cancel:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.btn-submit {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all var(--transition-fast);
}

.btn-submit:hover {
  background: var(--primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3);
}

.submit-icon {
  width: 16px;
  height: 16px;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-header {
    flex-direction: column;
    gap: 24px;
    text-align: center;
    padding: 30px 20px;
  }

  .hero-content {
    flex-direction: column;
  }

  .filter-section {
    margin: -20px 20px 20px;
    padding: 20px;
  }

  .category-tabs {
    flex-direction: column;
  }

  .tab-btn {
    width: 100%;
    justify-content: center;
  }

  .filter-bar {
    flex-direction: column;
  }

  .filter-select {
    width: 100%;
  }

  .resource-section {
    padding: 0 20px 20px;
  }

  .resource-grid {
    grid-template-columns: 1fr;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
