<template>
  <div class="page-container">
    <!-- Hero 区域 -->
    <section class="hero-section">
      <div class="hero-bg"></div>
      <div class="hero-content">
        <h1 class="hero-title">探索优质学习资源</h1>
        <p class="hero-subtitle">网络课程 · 校内资源 · 电子书籍，一站式学习平台</p>
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-number">{{ courses.length }}</span>
            <span class="stat-label">资源总数</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ courseTypes.length }}</span>
            <span class="stat-label">资源类型</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ getTotalDownloads() }}</span>
            <span class="stat-label">累计下载</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 分类卡片入口 -->
    <section v-if="!showResourceList" class="category-section">
      <h2 class="section-title">选择资源分类</h2>
      <div class="category-entrance">
        <div class="category-card" @click="enterCategory('online')">
          <div class="category-cover online-cover">
            <IconVideo class="category-icon" />
          </div>
          <div class="category-body">
            <h3>网络课程</h3>
            <p>精选优质在线课程资源</p>
            <div class="category-count">{{ getCount('online') }} 个资源</div>
          </div>
        </div>
        <div class="category-card" @click="enterCategory('campus')">
          <div class="category-cover campus-cover">
            <IconBook class="category-icon" />
          </div>
          <div class="category-body">
            <h3>校内课程</h3>
            <p>本校教师上传的课程资源</p>
            <div class="category-count">{{ getCount('campus') }} 个资源</div>
          </div>
        </div>
        <div class="category-card" @click="enterCategory('books')">
          <div class="category-cover books-cover">
            <IconDocument class="category-icon" />
          </div>
          <div class="category-body">
            <h3>书籍资源</h3>
            <p>电子书、文档等学习资料</p>
            <div class="category-count">{{ getCount('books') }} 个资源</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 资源列表页面 -->
    <section v-else class="resource-list-section">
      <div class="page-header">
        <button @click="backToCategories" class="btn-back">
          <IconArrowLeft class="btn-icon" />
          <span>返回分类</span>
        </button>
        <h2 class="page-title">{{ getCategoryTitle() }}</h2>
      </div>

      <!-- 筛选区域 -->
      <div class="filter-section glass">
        <div class="search-bar">
          <IconSearch class="search-icon" />
          <input
            v-model="searchText"
            :placeholder="getPlaceholder()"
            class="search-input"
          />
          <button v-if="searchText" @click="searchText = ''" class="clear-btn">
            <IconClose class="clear-icon" />
          </button>
        </div>

        <div class="quick-filters">
          <button
            @click="sortBy = 'downloads'"
            :class="['quick-filter', sortBy === 'downloads' ? 'active' : '']"
          >
            <IconStar class="filter-icon" />
            <span>热门</span>
          </button>
          <button
            @click="sortBy = 'newest'"
            :class="['quick-filter', sortBy === 'newest' ? 'active' : '']"
          >
            <IconClock class="filter-icon" />
            <span>最新</span>
          </button>
          <button
            @click="resetFilters"
            class="quick-filter reset"
          >
            <IconRefresh class="filter-icon" />
            <span>重置</span>
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
              <option v-for="t in filteredTypes" :key="t.id" :value="t.id">{{ t.name }}</option>
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
      </div>

      <!-- 资源网格 -->
      <div class="course-grid" v-if="loading">
        <div v-for="i in 6" :key="i" class="course-card skeleton">
          <div class="course-cover skeleton-cover"></div>
          <div class="course-body">
            <div class="skeleton-line title"></div>
            <div class="skeleton-line description"></div>
            <div class="skeleton-line meta"></div>
            <div class="skeleton-actions">
              <div class="skeleton-btn"></div>
              <div class="skeleton-btn"></div>
              <div class="skeleton-btn"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="course-grid" v-else>
        <div v-for="course in filteredCourses" :key="course.id" class="course-card" @click="viewDetails(course)">
          <!-- 卡片上半部分 - 封面图 -->
          <div class="course-cover" :class="getCoverClass(course.type_name)">
            <div class="cover-overlay"></div>
            <div class="cover-content">
              <component :is="getCoverIcon(course.type_name)" class="cover-icon" />
              <span class="cover-type">{{ course.type_name || '未分类' }}</span>
            </div>
            <div class="course-type-badge">{{ course.type_name || '未分类' }}</div>
          </div>

          <!-- 卡片下半部分 - 内容 -->
          <div class="course-body">
            <h3 class="course-title">{{ course.title }}</h3>
            <p class="course-description">{{ course.description }}</p>
            <div class="course-meta">
              <div class="meta-item">
                <IconUser class="meta-icon" />
                <span>{{ course.uploader?.name || course.uploader?.username || '未知' }}</span>
              </div>
              <div class="meta-item">
                <IconDownload class="meta-icon" />
                <span>{{ course.downloads }} 次下载</span>
              </div>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="course-actions" @click.stop>
            <button @click="toggleCollect(course)" :class="['btn-action', isCollected(course.id) ? 'collected' : '']" :title="isCollected(course.id) ? '已收藏' : '收藏'">
              <IconHeart class="action-icon" :class="{ filled: isCollected(course.id) }" />
            </button>
            <button @click="viewDetails(course)" class="btn-action btn-primary">
              <IconEye class="action-icon" />
              <span>详情</span>
            </button>
            <button @click="downloadCourse(course)" class="btn-action btn-primary">
              <IconDownload class="action-icon" />
              <span>下载</span>
            </button>
          </div>
        </div>

        <div v-if="filteredCourses.length === 0" class="empty-state">
          <IconFolder class="empty-icon" />
          <p>暂无课程数据</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import {
  IconVideo,
  IconBook,
  IconDocument,
  IconArrowLeft,
  IconSearch,
  IconClose,
  IconStar,
  IconClock,
  IconRefresh,
  IconCollection,
  IconSort,
  IconUser,
  IconDownload,
  IconHeart,
  IconEye,
  IconFolder
} from '../../components/icons'

const router = useRouter()

const courses = ref<any[]>([])
const courseTypes = ref<any[]>([])
const searchText = ref('')
const filterType = ref('')
const sortBy = ref('downloads')
const currentCategory = ref('')
const showResourceList = ref(false)
const collections = ref<any[]>([])
const loading = ref(true)

const filteredTypes = computed(() => {
  if (currentCategory.value === 'online') {
    return courseTypes.value.filter(type => type.name === '视频' || type.name === 'MOOC')
  } else if (currentCategory.value === 'campus') {
    return courseTypes.value.filter(type => type.name === '课件' || type.name === '作业')
  } else if (currentCategory.value === 'books') {
    return courseTypes.value.filter(type => type.name === '文档' || type.name === '电子书')
  }
  return courseTypes.value
})

const filteredCourses = computed(() => {
  let result = courses.value.filter(course => {
    const matchesSearch = course.title.toLowerCase().includes(searchText.value.toLowerCase()) ||
                         course.description.toLowerCase().includes(searchText.value.toLowerCase())
    const matchesType = !filterType.value || course.type === filterType.value

    let matchesTab = true
    if (currentCategory.value === 'online') {
      matchesTab = course.type_name === '视频' || course.type_name === 'MOOC'
    } else if (currentCategory.value === 'campus') {
      matchesTab = course.type_name === '课件' || course.type_name === '作业'
    } else if (currentCategory.value === 'books') {
      matchesTab = course.type_name === '文档' || course.type_name === '电子书'
    }

    return matchesSearch && matchesType && matchesTab
  })

  if (sortBy.value === 'downloads') {
    result.sort((a, b) => b.downloads - a.downloads)
  } else if (sortBy.value === 'newest') {
    result.sort((a, b) => new Date(b.upload_date).getTime() - new Date(a.upload_date).getTime())
  }

  return result
})

const fetchCourseTypes = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/courses/types/')
    courseTypes.value = response.data
  } catch (error) {
    console.error('获取课程类型失败', error)
  }
}

const fetchCourses = async () => {
  try {
    const token = localStorage.getItem('token')
    
    // 获取所有已审核通过的课程
    const response = await axios.get('http://127.0.0.1:8000/api/courses/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    // 只显示状态为 active 或 approved 的资源
    courses.value = response.data.filter((course: any) => {
      return course.status === 'active' || course.status === 'approved'
    })
  } catch (error) {
    console.error('获取课程列表失败', error)
  } finally {
    loading.value = false
  }
}

const enterCategory = (category: string) => {
  currentCategory.value = category
  showResourceList.value = true
}

const backToCategories = () => {
  showResourceList.value = false
}

const getCategoryTitle = () => {
  const titles: any = { online: '网络课程', campus: '校内课程', books: '书籍资源' }
  return titles[currentCategory.value] || '资源列表'
}

const getCount = (category: string) => {
  if (category === 'online') {
    return courses.value.filter(c => c.type_name === '视频' || c.type_name === 'MOOC').length
  } else if (category === 'campus') {
    return courses.value.filter(c => c.type_name === '课件' || c.type_name === '作业').length
  } else if (category === 'books') {
    return courses.value.filter(c => c.type_name === '文档' || c.type_name === '电子书').length
  }
  return 0
}

const getTotalDownloads = () => {
  return courses.value.reduce((sum, c) => sum + (c.downloads || 0), 0)
}

const fetchCollections = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/courses/collections/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    collections.value = response.data
  } catch (error) {
    console.error('获取收藏列表失败', error)
  }
}

const isCollected = (courseId: number) => {
  return collections.value.some(c => c.resource && c.resource.id === courseId)
}

const toggleCollect = async (course: any) => {
  try {
    const token = localStorage.getItem('token')

    if (isCollected(course.id)) {
      const collection = collections.value.find(c => c.resource && c.resource.id === course.id)
      if (collection) {
        await axios.delete(`http://127.0.0.1:8000/api/courses/uncollect/${collection.id}/`, {
          headers: { Authorization: `Bearer ${token}` }
        })
      }
      collections.value = collections.value.filter(c => c.resource && c.resource.id !== course.id)
      alert('已取消收藏')
    } else {
      await axios.post('http://127.0.0.1:8000/api/courses/collect/',
        { resource: course.id },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      await fetchCollections()
      alert('收藏成功')
    }
  } catch (error) {
    alert('操作失败')
  }
}

const viewDetails = (course: any) => {
  router.push(`/student/courses/${course.id}`)
}

const downloadCourse = async (course: any) => {
  try {
    const token = localStorage.getItem('token')
    await axios.post(`http://127.0.0.1:8000/api/courses/${course.id}/download/`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    })
    course.downloads += 1
    alert('下载成功！')
  } catch (error: any) {
    alert(error.response?.data?.error || '下载失败')
  }
}

const getPlaceholder = () => {
  if (currentCategory.value === 'online') {
    return '搜索网络课程...'
  } else if (currentCategory.value === 'campus') {
    return '搜索校内课程...'
  } else {
    return '搜索书籍...'
  }
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
  return iconMap[typeName] || IconBook
}

const resetFilters = () => {
  searchText.value = ''
  filterType.value = ''
  sortBy.value = 'downloads'
}

onMounted(() => {
  fetchCourseTypes()
  fetchCourses()
  fetchCollections()
})
</script>

<style scoped>
.page-container {
  padding: 0;
  background: var(--bg-color);
  min-height: calc(100vh - 64px);
}

/* Hero 区域 */
.hero-section {
  position: relative;
  padding: 80px 40px;
  text-align: center;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(13, 148, 136, 0.1) 0%, rgba(20, 184, 166, 0.05) 100%);
  z-index: 0;
}

.hero-bg::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="%230d9488" opacity="0.1"/><circle cx="80" cy="40" r="3" fill="%230d9488" opacity="0.1"/><circle cx="40" cy="80" r="2" fill="%230d9488" opacity="0.1"/><circle cx="70" cy="70" r="4" fill="%230d9488" opacity="0.1"/></svg>');
  background-size: 200px 200px;
  opacity: 0.5;
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 16px;
  font-family: var(--font-sf);
  letter-spacing: -1px;
}

.hero-subtitle {
  font-size: 18px;
  color: var(--text-secondary);
  margin: 0 0 40px;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 60px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.stat-number {
  font-size: 36px;
  font-weight: 700;
  color: var(--primary-color);
  font-family: var(--font-sf);
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
}

/* 分类区域 */
.category-section {
  padding: 40px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 30px;
  font-family: var(--font-sf);
}

.category-entrance {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 30px;
}

.category-card {
  background: white;
  border-radius: var(--border-radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  cursor: pointer;
  transition: all var(--transition-normal);
  border: 1px solid var(--border-light);
}

.category-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-xl);
}

.category-cover {
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.online-cover {
  background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%);
}

.campus-cover {
  background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);
}

.books-cover {
  background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
}

.category-icon {
  width: 80px;
  height: 80px;
  color: white;
  opacity: 0.9;
}

.category-body {
  padding: 24px;
  text-align: center;
}

.category-body h3 {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 8px;
}

.category-body p {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0 0 16px;
}

.category-count {
  display: inline-block;
  padding: 8px 20px;
  background: var(--bg-tertiary);
  color: var(--primary-color);
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

/* 资源列表区域 */
.resource-list-section {
  padding: 40px;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: white;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  transition: all var(--transition-fast);
}

.btn-back:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
  transform: translateX(-4px);
}

.btn-icon {
  width: 18px;
  height: 18px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  font-family: var(--font-sf);
}

/* 筛选区域 */
.filter-section {
  padding: 24px;
  border-radius: var(--border-radius-xl);
  margin-bottom: 30px;
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

.quick-filters {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.quick-filter {
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

.filter-icon {
  width: 16px;
  height: 16px;
}

.quick-filter:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
  transform: translateY(-2px);
}

.quick-filter.active {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.quick-filter.reset {
  margin-left: auto;
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

/* 课程网格 */
.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 30px;
}

.course-card {
  background: white;
  border-radius: var(--border-radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  transition: all var(--transition-normal);
  border: 1px solid var(--border-light);
  cursor: pointer;
}

.course-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-xl);
}

/* 卡片封面 - 上半部分 */
.course-cover {
  position: relative;
  height: 200px;
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

.cover-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.cover-icon {
  width: 64px;
  height: 64px;
  color: white;
  opacity: 0.9;
}

.cover-type {
  font-size: 14px;
  font-weight: 500;
  color: white;
  padding: 6px 16px;
  background: rgba(255,255,255,0.2);
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

.course-type-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  padding: 6px 14px;
  background: rgba(255,255,255,0.95);
  color: var(--primary-color);
  border-radius: var(--border-radius-sm);
  font-size: 12px;
  font-weight: 600;
  backdrop-filter: blur(10px);
}

/* 卡片内容 - 下半部分 */
.course-body {
  padding: 24px;
}

.course-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 12px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.course-description {
  color: var(--text-secondary);
  font-size: 14px;
  margin: 0 0 16px;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.course-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: 16px;
  border-top: 1px solid var(--border-light);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-secondary);
}

.meta-icon {
  width: 16px;
  height: 16px;
  color: var(--text-tertiary);
}

/* 操作按钮 */
.course-actions {
  display: flex;
  gap: 8px;
  padding: 0 24px 24px;
}

.btn-action {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background: white;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-action:hover {
  transform: translateY(-2px);
}

.action-icon {
  width: 18px;
  height: 18px;
}

.action-icon.filled {
  fill: currentColor;
}

.btn-action.collected {
  background: #fef2f2;
  border-color: #fecaca;
  color: #ef4444;
}

.btn-action.collected .action-icon {
  fill: currentColor;
}

.btn-primary {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  background: var(--primary-dark);
  border-color: var(--primary-dark);
  box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3);
}

/* 空状态 */
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

/* 骨架屏 */
.skeleton {
  pointer-events: none;
}

.skeleton-cover {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
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

.skeleton-line.description {
  height: 16px;
  width: 100%;
}

.skeleton-line.meta {
  height: 14px;
  width: 60%;
}

.skeleton-actions {
  display: flex;
  gap: 8px;
  margin-top: 16px;
}

.skeleton-btn {
  flex: 1;
  height: 40px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
  border-radius: var(--border-radius);
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-section {
    padding: 60px 20px;
  }

  .hero-title {
    font-size: 32px;
  }

  .hero-stats {
    gap: 30px;
  }

  .stat-number {
    font-size: 28px;
  }

  .category-section,
  .resource-list-section {
    padding: 20px;
  }

  .category-entrance {
    grid-template-columns: 1fr;
  }

  .course-grid {
    grid-template-columns: 1fr;
  }

  .filter-bar {
    flex-direction: column;
  }

  .filter-select {
    width: 100%;
  }

  .quick-filter.reset {
    margin-left: 0;
    width: 100%;
  }
}
</style>
