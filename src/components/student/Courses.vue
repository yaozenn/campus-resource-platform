<template>
  <div class="page-container">
    <section class="hero-section">
      <div class="hero-bg"></div>
      <div class="hero-content">
        <h1 class="hero-title">探索优质学习资源</h1>
        <p class="hero-subtitle">课程资料 · 网络拓展 · 电子书籍，一站式师生共享平台</p>
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-number">{{ courses.length }}</span>
            <span class="stat-label">资源总数</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ courseTypes.length }}</span>
            <span class="stat-label">细分类型</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ getTotalDownloads() }}</span>
            <span class="stat-label">累计下载</span>
          </div>
        </div>
      </div>
    </section>

    <section v-if="!showResourceList" class="category-section fade-in">
      <h2 class="section-title">选择资源分类</h2>
      <div class="category-entrance">
        <div v-for="cat in mainCategories" :key="cat.id" class="category-card" @click="enterCategory(cat.id)">
          <div class="category-cover" :class="cat.coverClass">
            <component :is="cat.icon" class="category-icon" />
          </div>
          <div class="category-body">
            <h3>{{ cat.title }}</h3>
            <p>{{ cat.desc }}</p>
            <div class="category-count">{{ getCount(cat.id) }} 个资源</div>
          </div>
        </div>
      </div>
    </section>

    <section v-else class="resource-list-section fade-in">
      <div class="page-header">
        <button @click="backToCategories" class="btn-back">
          <IconArrowLeft class="btn-icon" />
          <span>返回分类</span>
        </button>
        <h2 class="page-title">{{ currentCategory }}</h2>
      </div>

      <div class="filter-section glass">
        <div class="search-bar">
          <IconSearch class="search-icon" />
          <input
            v-model="searchText"
            :placeholder="`在 ${currentCategory} 中搜索...`"
            class="search-input"
          />
          <button v-if="searchText" @click="searchText = ''" class="clear-btn">
            <IconClose class="clear-icon" />
          </button>
        </div>

        <div class="quick-filters">
          <button @click="sortBy = 'downloads'" :class="['quick-filter', sortBy === 'downloads' ? 'active' : '']">
            <IconStar class="filter-icon" /> <span>热门</span>
          </button>
          <button @click="sortBy = 'newest'" :class="['quick-filter', sortBy === 'newest' ? 'active' : '']">
            <IconClock class="filter-icon" /> <span>最新</span>
          </button>
          <button @click="resetFilters" class="quick-filter reset">
            <IconRefresh class="filter-icon" /> <span>重置</span>
          </button>
        </div>

        <div class="filter-bar">
          <div class="filter-group">
            <label class="filter-label">
              <IconCollection class="label-icon" /> <span>具体分类</span>
            </label>
            <select v-model="filterType" class="filter-select">
              <option value="">全部类型</option>
              <option v-for="t in filteredTypes" :key="t.id" :value="t.id">{{ t.name }}</option>
            </select>
          </div>

          <div class="filter-group">
            <label class="filter-label">
              <IconSort class="label-icon" /> <span>排序</span>
            </label>
            <select v-model="sortBy" class="filter-select">
              <option value="downloads">下载最多</option>
              <option value="newest">最新上传</option>
            </select>
          </div>
        </div>
      </div>

      <div class="course-grid" v-if="loading">
        <div v-for="i in 6" :key="i" class="course-card skeleton">
          <div class="course-cover skeleton-cover"></div>
          <div class="course-body">
            <div class="skeleton-line title"></div>
            <div class="skeleton-line description"></div>
            <div class="skeleton-line meta"></div>
          </div>
        </div>
      </div>

      <div class="course-grid" v-else>
        <div v-for="course in filteredCourses" :key="course.id" class="course-card" @click="viewDetails(course)">
          
          <div class="course-cover" :class="getCoverClassByMain(currentCategory)">
            <div class="cover-overlay"></div>
            <div class="cover-content">
              <component :is="getIconByMain(currentCategory)" class="cover-icon" />
              <span class="cover-type">{{ course.type_name || '未分类' }}</span>
            </div>
            
            <div v-if="course.is_second_hand" class="second-hand-badge">
              二手闲置 ¥{{ course.price }}
            </div>
          </div>

          <div class="course-body">
            <h3 class="course-title">{{ course.title }}</h3>
            <p class="course-description">{{ course.description || '暂无描述' }}</p>
            <div class="course-meta">
              <div class="meta-item">
                <IconUser class="meta-icon" />
                <span :class="{'teacher-tag': course.uploader?.role === 'teacher'}">
                  {{ course.uploader?.name || course.uploader?.username || '未知' }}
                  <span v-if="course.uploader?.role === 'teacher'">(认证教师)</span>
                </span>
              </div>
              <div class="meta-item">
                <IconDownload class="meta-icon" />
                <span>{{ course.downloads }} 次下载</span>
              </div>
            </div>
          </div>

          <div class="course-actions" @click.stop>
            <button @click="toggleCollect(course)" :class="['btn-action', isCollected(course.id) ? 'collected' : '']" :title="isCollected(course.id) ? '已收藏' : '收藏'">
              <IconHeart class="action-icon" :class="{ filled: isCollected(course.id) }" />
            </button>
            <button @click="viewDetails(course)" class="btn-action btn-primary">
              <IconEye class="action-icon" /> <span>详情</span>
            </button>
            <button @click="downloadCourse(course)" class="btn-action btn-primary">
              <IconDownload class="action-icon" /> <span>下载</span>
            </button>
          </div>
        </div>

        <div v-if="filteredCourses.length === 0" class="empty-state">
          <IconFolder class="empty-icon" />
          <p>该分类下暂无资源，快去“我的分享”发布一个吧！</p>
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
  IconVideo, IconBook, IconDocument, IconArrowLeft, IconSearch, IconClose,
  IconStar, IconClock, IconRefresh, IconCollection, IconSort, IconUser,
  IconDownload, IconHeart, IconEye, IconFolder
} from '../../components/icons'

const router = useRouter()

const courses = ref<any[]>([])
const courseTypes = ref<any[]>([])
const collections = ref<any[]>([])
const loading = ref(true)

const searchText = ref('')
const filterType = ref('')
const sortBy = ref('downloads')
const currentCategory = ref('') // 存储当前选中的大类 (description)
const showResourceList = ref(false)

// 定义前端展示的三大主类
const mainCategories = [
  { id: '课程资源', title: '课程资源', desc: '紧贴校内教学，课件与真题', icon: IconBook, coverClass: 'campus-cover' },
  { id: '网络资源', title: '网络资源', desc: '拓展课外视野，网课与工具', icon: IconVideo, coverClass: 'online-cover' },
  { id: '书籍资源', title: '书籍资源', desc: '教材与辅导资料，含二手流转', icon: IconDocument, coverClass: 'books-cover' }
]

// 根据当前大类，筛选出对应的细分类型下拉选项
const filteredTypes = computed(() => {
  return courseTypes.value.filter(t => t.description === currentCategory.value)
})

// 根据大类和具体筛选条件，过滤课程
const filteredCourses = computed(() => {
  let result = courses.value.filter(course => {
    // 1. 搜索匹配
    const matchesSearch = course.title.toLowerCase().includes(searchText.value.toLowerCase()) ||
                         (course.description || '').toLowerCase().includes(searchText.value.toLowerCase())
    
    // 2. 细分类型匹配
    const matchesSubType = !filterType.value || course.type === filterType.value

    // 3. 大类匹配: 找到这个资源的type对应的description
    const courseTypeObj = courseTypes.value.find(t => t.id === course.type)
    const courseMainCat = courseTypeObj ? courseTypeObj.description : '其他未分类'
    const matchesMainCat = !currentCategory.value || courseMainCat === currentCategory.value

    return matchesSearch && matchesSubType && matchesMainCat
  })

  // 排序
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
  } catch (error) { console.error('获取课程类型失败', error) }
}

const fetchCourses = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/courses/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    courses.value = response.data.filter((course: any) => course.status === 'active' || course.status === 'approved')
  } catch (error) {
    console.error('获取课程列表失败', error)
  } finally {
    loading.value = false
  }
}

// 统计大类下有多少资源
const getCount = (mainCatId: string) => {
  return courses.value.filter(course => {
    const typeObj = courseTypes.value.find(t => t.id === course.type)
    return typeObj && typeObj.description === mainCatId
  }).length
}

const enterCategory = (categoryId: string) => {
  currentCategory.value = categoryId
  showResourceList.value = true
  filterType.value = '' // 进入新大类时重置细分类
}
const backToCategories = () => { showResourceList.value = false }
const getTotalDownloads = () => courses.value.reduce((sum, c) => sum + (c.downloads || 0), 0)

const fetchCollections = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/courses/collections/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    collections.value = response.data
  } catch (error) { console.error('获取收藏列表失败', error) }
}

const isCollected = (courseId: number) => collections.value.some(c => c.resource && c.resource.id === courseId)

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
      await axios.post('http://127.0.0.1:8000/api/courses/collect/', { resource: course.id }, { headers: { Authorization: `Bearer ${token}` } })
      await fetchCollections()
      alert('收藏成功')
    }
  } catch (error) { alert('操作失败') }
}

const viewDetails = (course: any) => router.push(`/student/courses/${course.id}`)
const downloadCourse = async (course: any) => {
  try {
    const token = localStorage.getItem('token')
    await axios.post(`http://127.0.0.1:8000/api/courses/${course.id}/download/`, {}, { headers: { Authorization: `Bearer ${token}` } })
    course.downloads += 1
    alert('下载成功！')
  } catch (error: any) { alert(error.response?.data?.error || '下载失败') }
}

const resetFilters = () => {
  searchText.value = ''
  filterType.value = ''
  sortBy.value = 'downloads'
}

// 动态样式辅助函数
const getCoverClassByMain = (mainCat: string) => {
  if (mainCat === '课程资源') return 'cover-courseware'
  if (mainCat === '网络资源') return 'cover-video'
  if (mainCat === '书籍资源') return 'cover-ebook'
  return 'cover-default'
}

const getIconByMain = (mainCat: string) => {
  if (mainCat === '课程资源') return IconBook
  if (mainCat === '网络资源') return IconVideo
  if (mainCat === '书籍资源') return IconDocument
  return IconBook
}

onMounted(() => {
  fetchCourseTypes()
  fetchCourses()
  fetchCollections()
})
</script>

<style scoped>
.page-container { padding: 0; background: var(--bg-color); min-height: calc(100vh - 64px); }

/* Hero 区域 */
.hero-section { position: relative; padding: 80px 40px; text-align: center; overflow: hidden; }
.hero-bg { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(135deg, rgba(13, 148, 136, 0.1) 0%, rgba(20, 184, 166, 0.05) 100%); z-index: 0; }
.hero-bg::before { content: ''; position: absolute; inset: 0; background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="%230d9488" opacity="0.1"/><circle cx="80" cy="40" r="3" fill="%230d9488" opacity="0.1"/><circle cx="40" cy="80" r="2" fill="%230d9488" opacity="0.1"/><circle cx="70" cy="70" r="4" fill="%230d9488" opacity="0.1"/></svg>'); background-size: 200px 200px; opacity: 0.5; }
.hero-content { position: relative; z-index: 1; max-width: 800px; margin: 0 auto; }
.hero-title { font-size: 48px; font-weight: 700; color: var(--text-primary); margin: 0 0 16px; font-family: var(--font-sf); letter-spacing: -1px; }
.hero-subtitle { font-size: 18px; color: var(--text-secondary); margin: 0 0 40px; }
.hero-stats { display: flex; justify-content: center; gap: 60px; }
.stat-item { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.stat-number { font-size: 36px; font-weight: 700; color: var(--primary-color); font-family: var(--font-sf); }
.stat-label { font-size: 14px; color: var(--text-secondary); }

/* 分类入口区域 */
.category-section { padding: 40px; max-width: 1200px; margin: 0 auto;}
.section-title { font-size: 24px; font-weight: 600; color: var(--text-primary); margin: 0 0 30px; font-family: var(--font-sf); }
.category-entrance { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 30px; }
.category-card { background: white; border-radius: var(--border-radius-xl); overflow: hidden; box-shadow: var(--shadow-sm); cursor: pointer; transition: all var(--transition-normal); border: 1px solid var(--border-light); }
.category-card:hover { transform: translateY(-8px); box-shadow: var(--shadow-xl); border-color: var(--primary-color); }
.category-cover { height: 180px; display: flex; align-items: center; justify-content: center; position: relative; }

/* 三大主类封面颜色 */
.campus-cover { background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%); }
.online-cover { background: linear-gradient(135deg, #0ea5e9 0%, #38bdf8 100%); }
.books-cover { background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%); }

.category-icon { width: 80px; height: 80px; color: white; opacity: 0.9; }
.category-body { padding: 24px; text-align: center; }
.category-body h3 { font-size: 20px; font-weight: 600; color: var(--text-primary); margin: 0 0 8px; }
.category-body p { font-size: 14px; color: var(--text-secondary); margin: 0 0 16px; }
.category-count { display: inline-block; padding: 8px 20px; background: var(--primary-soft); color: var(--primary-dark); border-radius: 20px; font-size: 14px; font-weight: 600; }

/* 资源列表区域 */
.resource-list-section { padding: 40px; max-width: 1200px; margin: 0 auto;}
.page-header { display: flex; align-items: center; gap: 20px; margin-bottom: 30px; }
.btn-back { display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; background: white; border: 1px solid var(--border-color); border-radius: var(--border-radius-lg); cursor: pointer; font-size: 14px; font-weight: 500; color: var(--text-secondary); transition: all var(--transition-fast); }
.btn-back:hover { border-color: var(--primary-color); color: var(--primary-color); transform: translateX(-4px); }
.page-title { font-size: 28px; font-weight: 700; color: var(--text-primary); margin: 0; font-family: var(--font-sf); }

/* 筛选与搜索 */
.filter-section { padding: 24px; border-radius: var(--border-radius-xl); margin-bottom: 30px; }
.search-bar { position: relative; display: flex; align-items: center; margin-bottom: 20px; }
.search-icon { position: absolute; left: 16px; width: 20px; height: 20px; color: var(--text-placeholder); }
.search-input { width: 100%; padding: 14px 48px; border: 2px solid var(--border-color); border-radius: var(--border-radius-lg); font-size: 15px; transition: all var(--transition-fast); background: white; }
.search-input:focus { outline: none; border-color: var(--primary-color); box-shadow: 0 0 0 4px rgba(13, 148, 136, 0.1); }
.clear-btn { position: absolute; right: 12px; width: 32px; height: 32px; border: none; background: var(--bg-tertiary); border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.clear-btn:hover { background: var(--primary-color); color: white; }
.quick-filters { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
.quick-filter { display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; background: white; border: 1px solid var(--border-color); border-radius: var(--border-radius); color: var(--text-secondary); font-size: 14px; cursor: pointer; transition: all 0.2s; }
.quick-filter:hover { border-color: var(--primary-color); color: var(--primary-color); transform: translateY(-2px); }
.quick-filter.active { background: var(--primary-color); border-color: var(--primary-color); color: white; }
.quick-filter.reset { margin-left: auto; }
.filter-bar { display: flex; gap: 24px; flex-wrap: wrap; }
.filter-group { display: flex; align-items: center; gap: 12px; }
.filter-label { display: flex; align-items: center; gap: 8px; color: var(--text-secondary); font-size: 14px; font-weight: 500; }
.filter-select { padding: 10px 40px 10px 16px; border: 1px solid var(--border-color); border-radius: var(--border-radius); min-width: 160px; font-size: 14px; background: white; cursor: pointer; appearance: none; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23909399' d='M6 9L1 4h10z'/%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 12px center; }
.filter-select:focus { outline: none; border-color: var(--primary-color); box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1); }

/* 课程网格 */
.course-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 30px; }
.course-card { background: white; border-radius: var(--border-radius-xl); overflow: hidden; box-shadow: var(--shadow-sm); border: 1px solid var(--border-light); cursor: pointer; transition: all 0.3s; }
.course-card:hover { transform: translateY(-8px); box-shadow: var(--shadow-xl); border-color: var(--primary-light); }

.course-cover { position: relative; height: 180px; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.cover-video { background: linear-gradient(135deg, #0ea5e9 0%, #38bdf8 100%); }
.cover-courseware { background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%); }
.cover-ebook { background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%); }
.cover-default { background: linear-gradient(135deg, #6b7280 0%, #9ca3af 100%); }

.cover-overlay { position: absolute; inset: 0; background: linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.4) 100%); }
.cover-content { position: relative; z-index: 1; display: flex; flex-direction: column; align-items: center; gap: 12px; }
.cover-icon { width: 56px; height: 56px; color: white; opacity: 0.9; }
.cover-type { font-size: 13px; font-weight: 500; color: white; padding: 4px 16px; background: rgba(255,255,255,0.25); border-radius: 20px; backdrop-filter: blur(10px); }

/* 二手专属标签 */
.second-hand-badge { position: absolute; top: 12px; right: 12px; padding: 6px 12px; background: linear-gradient(135deg, #f59e0b, #fbbf24); color: white; border-radius: 8px; font-size: 13px; font-weight: 700; box-shadow: 0 4px 10px rgba(0,0,0,0.15); z-index: 2; border: 1px solid rgba(255,255,255,0.3); }

.course-body { padding: 24px; }
.course-title { font-size: 18px; font-weight: 600; color: var(--text-primary); margin: 0 0 12px; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden; }
.course-description { color: var(--text-secondary); font-size: 14px; margin: 0 0 16px; line-height: 1.6; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 44px;}

.course-meta { display: flex; flex-direction: column; gap: 8px; padding-top: 16px; border-top: 1px solid var(--border-light); }
.meta-item { display: flex; align-items: center; gap: 8px; font-size: 13px; color: var(--text-secondary); }
.meta-icon { width: 16px; height: 16px; color: var(--text-tertiary); }
.teacher-tag { color: var(--primary-color); font-weight: 600; background: var(--primary-soft); padding: 2px 8px; border-radius: 4px;}

.course-actions { display: flex; gap: 8px; padding: 0 24px 24px; }
.btn-action { flex: 1; display: inline-flex; align-items: center; justify-content: center; gap: 6px; padding: 10px; border: 1px solid var(--border-color); border-radius: var(--border-radius); background: white; color: var(--text-secondary); font-size: 13px; font-weight: 500; cursor: pointer; transition: all 0.2s; }
.btn-action:hover { transform: translateY(-2px); border-color: var(--primary-color); color: var(--primary-color); }
.btn-action.collected { background: #fef2f2; border-color: #fca5a5; color: #ef4444; }
.btn-primary { background: var(--primary-color); border-color: var(--primary-color); color: white; }
.btn-primary:hover { background: var(--primary-dark); color: white; box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3); }

.empty-state { grid-column: 1 / -1; text-align: center; padding: 80px 20px; color: var(--text-placeholder); }
.empty-icon { width: 80px; height: 80px; margin: 0 auto 20px; color: var(--text-tertiary); }

.fade-in { animation: fadeIn var(--transition-normal); }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

@media (max-width: 768px) {
  .hero-section { padding: 60px 20px; }
  .hero-title { font-size: 32px; }
  .category-entrance { grid-template-columns: 1fr; }
  .course-grid { grid-template-columns: 1fr; }
}
</style>