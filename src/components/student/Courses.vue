<template>
  <div class="page-container">
    <section class="hero-section">
      <div class="hero-bg"></div>
      <div class="hero-content">
        <h1 class="hero-title">探索优质学习资源</h1>
        <p class="hero-subtitle">课程资料 · 网络拓展 · 电子书籍，一站式师生共享平台</p>
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-number">{{ validCourses.length }}</span>
            <span class="stat-label">有效资源</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ activeMainCategoriesCount }}</span>
            <span class="stat-label">活跃分类</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ totalValidDownloads }}</span>
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
            <div v-if="course.is_second_hand" class="second-hand-badge">二手闲置 ¥{{ course.price }}</div>
          </div>

          <div class="course-body">
            <h3 class="course-title">{{ course.title }}</h3>
            <p class="course-description">{{ course.description || '暂无描述' }}</p>
            <div class="course-meta">
              <div class="meta-item">
                <IconUser class="meta-icon" />
                <span :class="{'teacher-tag': (course.uploader_info?.role || course.uploader?.role) === 'teacher'}">
                  {{ course.uploader_name || course.uploader_username || course.uploader_info?.name || course.uploader_info?.username || course.uploader?.name || course.uploader?.username || '未知' }}
                  <span v-if="(course.uploader_info?.role || course.uploader?.role) === 'teacher'">(认证教师)</span>
                </span>
              </div>
              <div class="meta-item">
                <IconDownload class="meta-icon" />
                <span>{{ course.downloads }} 次下载</span>
              </div>
            </div>
          </div>

          <div class="course-actions" @click.stop>
            <button @click="toggleCollect(course)" :class="['btn-action', isCollected(course.id) ? 'collected' : '']">
              <IconHeart class="action-icon" :filled="isCollected(course.id)" />
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
import { useToast } from '../../composables/useToast'
import {
  IconVideo, IconBook, IconDocument, IconArrowLeft, IconSearch, IconClose,
  IconStar, IconClock, IconRefresh, IconCollection, IconSort, IconUser,
  IconDownload, IconHeart, IconEye, IconFolder
} from '../../components/icons'

const toast = useToast()
const router = useRouter()

const courses = ref<any[]>([])
const courseTypes = ref<any[]>([])
const collections = ref<any[]>([])
const loading = ref(true)

const searchText = ref('')
const filterType = ref('')
const sortBy = ref('downloads')
const currentCategory = ref('') 
const showResourceList = ref(false)

const mainCategories = [
  { id: '课程资源', title: '课程资源', desc: '紧贴校内教学，课件与真题', icon: IconBook, coverClass: 'campus-cover' },
  { id: '网络资源', title: '网络资源', desc: '拓展课外视野，网课与工具', icon: IconVideo, coverClass: 'online-cover' },
  { id: '书籍资源', title: '书籍资源', desc: '教材与辅导资料，含二手流转', icon: IconDocument, coverClass: 'books-cover' }
]

// 核心修复：仅统计符合新分类标准的有效资源，过滤历史残留数据
const validCourses = computed(() => {
  return courses.value.filter(course => {
    const typeObj = courseTypes.value.find(t => t.id === course.type)
    return typeObj && ['课程资源', '网络资源', '书籍资源'].includes(typeObj.description)
  })
})

const activeMainCategoriesCount = computed(() => {
  const descriptions = courseTypes.value.map(t => t.description)
  return new Set(descriptions.filter(d => ['课程资源', '网络资源', '书籍资源'].includes(d))).size
})

const totalValidDownloads = computed(() => {
  return validCourses.value.reduce((sum, c) => sum + (c.downloads || 0), 0)
})

const filteredTypes = computed(() => {
  return courseTypes.value.filter(t => t.description === currentCategory.value)
})

const filteredCourses = computed(() => {
  let result = validCourses.value.filter(course => {
    const matchesSearch = course.title.toLowerCase().includes(searchText.value.toLowerCase()) ||
                         (course.description || '').toLowerCase().includes(searchText.value.toLowerCase())
    const matchesSubType = !filterType.value || course.type === filterType.value
    const typeObj = courseTypes.value.find(t => t.id === course.type)
    const matchesMainCat = typeObj?.description === currentCategory.value
    return matchesSearch && matchesSubType && matchesMainCat
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
  } catch (error) { console.error('获取课程类型失败', error) }
}

const fetchCourses = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/courses/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    courses.value = response.data.filter((course: any) => course.status === 'active')
  } catch (error) {
    console.error('获取课程列表失败', error)
  } finally {
    loading.value = false
  }
}

const fetchCollections = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/courses/collections/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    collections.value = response.data
  } catch (error) { console.error('获取收藏列表失败', error) }
}

const getCount = (mainCatId: string) => {
  return validCourses.value.filter(course => {
    const typeObj = courseTypes.value.find(t => t.id === course.type)
    return typeObj?.description === mainCatId
  }).length
}

const downloadCourse = async (course: any) => {
  try {
    const token = localStorage.getItem('token')
    // 修复点：调用后端 /download/ 接口增加下载统计
    const res = await axios.post(`http://127.0.0.1:8000/api/courses/${course.id}/download/`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (res.data.file_url) {
      window.open(res.data.file_url, '_blank')
      course.downloads += 1
      toast.success('下载已开始')
    }
  } catch (error: any) { toast.error(error.response?.data?.error || '下载失败') }
}

const isCollected = (courseId: number) => collections.value.some(c => c.resource?.id === courseId)

const toggleCollect = async (course: any) => {
  const token = localStorage.getItem('token')
  try {
    if (isCollected(course.id)) {
      const collection = collections.value.find(c => c.resource?.id === course.id)
      await axios.delete(`http://127.0.0.1:8000/api/courses/uncollect/${collection.id}/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      collections.value = collections.value.filter(c => c.id !== collection.id)
      toast.success('已取消收藏')
    } else {
      await axios.post('http://127.0.0.1:8000/api/courses/collect/', { resource: course.id }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      await fetchCollections()
      toast.success('收藏成功')
    }
  } catch (error) { toast.error('操作失败') }
}

const enterCategory = (categoryId: string) => { currentCategory.value = categoryId; showResourceList.value = true; filterType.value = '' }
const backToCategories = () => { showResourceList.value = false }
const viewDetails = (course: any) => router.push(`/student/courses/${course.id}`)
const resetFilters = () => { searchText.value = ''; filterType.value = ''; sortBy.value = 'downloads' }

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

onMounted(() => { fetchCourseTypes(); fetchCourses(); fetchCollections() })
</script>

<style scoped>
.page-container { padding: 0; background: var(--bg-color); min-height: calc(100vh - 64px); }
.hero-section { position: relative; padding: 80px 40px; text-align: center; overflow: hidden; }
.hero-bg { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(135deg, rgba(13, 148, 136, 0.1) 0%, rgba(20, 184, 166, 0.05) 100%); z-index: 0; }
.hero-content { position: relative; z-index: 1; max-width: 800px; margin: 0 auto; }
.hero-title { font-size: 48px; font-weight: 700; color: var(--text-primary); margin: 0 0 16px; letter-spacing: -1px; }
.hero-subtitle { font-size: 18px; color: var(--text-secondary); margin: 0 0 40px; }
.hero-stats { display: flex; justify-content: center; gap: 60px; }
.stat-item { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.stat-number { font-size: 36px; font-weight: 700; color: var(--primary-color); }
.stat-label { font-size: 14px; color: var(--text-secondary); }

.category-section { padding: 40px; max-width: 1200px; margin: 0 auto;}
.section-title { font-size: 24px; font-weight: 600; color: var(--text-primary); margin: 0 0 30px; }
.category-entrance { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 30px; }
.category-card { background: white; border-radius: var(--border-radius-xl); overflow: hidden; box-shadow: var(--shadow-sm); cursor: pointer; transition: all 0.3s; border: 1px solid var(--border-light); }
.category-card:hover { transform: translateY(-8px); box-shadow: var(--shadow-xl); border-color: var(--primary-color); }
.category-cover { height: 180px; display: flex; align-items: center; justify-content: center; }
.campus-cover { background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%); }
.online-cover { background: linear-gradient(135deg, #0ea5e9 0%, #38bdf8 100%); }
.books-cover { background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%); }
.category-icon { width: 80px; height: 80px; color: white; opacity: 0.9; }
.category-body { padding: 24px; text-align: center; }
.category-body h3 { font-size: 20px; font-weight: 600; color: var(--text-primary); margin: 0 0 8px; }
.category-count { display: inline-block; padding: 8px 20px; background: var(--primary-soft); color: var(--primary-dark); border-radius: 20px; font-size: 14px; font-weight: 600; }

.resource-list-section { padding: 40px; max-width: 1200px; margin: 0 auto;}
.page-header { display: flex; align-items: center; gap: 20px; margin-bottom: 30px; }
.btn-back { display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; background: white; border: 1px solid var(--border-color); border-radius: var(--border-radius-lg); cursor: pointer; }
.page-title { font-size: 28px; font-weight: 700; color: var(--text-primary); margin: 0; }

.filter-section { padding: 24px; border-radius: var(--border-radius-xl); margin-bottom: 30px; background: rgba(255,255,255,0.8); backdrop-filter: blur(10px); }
.search-bar { position: relative; display: flex; align-items: center; margin-bottom: 20px; }
.search-icon { position: absolute; left: 16px; width: 20px; height: 20px; color: var(--text-placeholder); }
.search-input { width: 100%; padding: 14px 48px; border: 2px solid var(--border-color); border-radius: var(--border-radius-lg); font-size: 15px; }
.quick-filters { display: flex; gap: 12px; margin-bottom: 20px; }
.quick-filter { display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; background: white; border: 1px solid var(--border-color); border-radius: var(--border-radius); cursor: pointer; }
.quick-filter.active { background: var(--primary-color); color: white; }
.filter-bar { display: flex; gap: 24px; }
.filter-group { display: flex; align-items: center; gap: 12px; }
.filter-label { display: flex; align-items: center; gap: 6px; font-size: 14px; font-weight: 500; color: var(--text-secondary); }
.label-icon { width: 16px; height: 16px; }
.filter-select {
  padding: 10px 36px 10px 14px;
  border: 2px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: 14px;
  background: white url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%236b7280' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E") no-repeat right 12px center;
  appearance: none;
  cursor: pointer;
  min-width: 140px;
  transition: all 0.2s;
}
.filter-select:hover { border-color: var(--primary-color); }
.filter-select:focus { outline: none; border-color: var(--primary-color); box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1); }

.course-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 30px; }
.course-card { background: white; border-radius: var(--border-radius-xl); overflow: hidden; box-shadow: var(--shadow-sm); border: 1px solid var(--border-light); cursor: pointer; transition: all 0.3s; }
.course-card:hover { transform: translateY(-8px); box-shadow: var(--shadow-xl); }
.course-cover { position: relative; height: 180px; display: flex; align-items: center; justify-content: center; }
.cover-video { background: linear-gradient(135deg, #0ea5e9 0%, #38bdf8 100%); }
.cover-courseware { background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%); }
.cover-ebook { background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%); }
.cover-overlay { position: absolute; inset: 0; background: linear-gradient(to bottom, transparent, rgba(0,0,0,0.4)); }
.cover-content { position: relative; z-index: 1; display: flex; flex-direction: column; align-items: center; gap: 12px; color: white; }
.cover-icon { width: 56px; height: 56px; }
.cover-type { font-size: 13px; padding: 4px 16px; background: rgba(255,255,255,0.2); border-radius: 20px; }
.second-hand-badge { position: absolute; top: 12px; right: 12px; padding: 6px 12px; background: #f59e0b; color: white; border-radius: 8px; font-weight: 700; z-index: 2; }

.course-body { padding: 24px; }
.course-title { font-size: 18px; font-weight: 600; margin: 0 0 12px; }
.course-description { color: var(--text-secondary); font-size: 14px; height: 44px; overflow: hidden; }
.course-meta { display: flex; flex-direction: column; gap: 8px; padding-top: 16px; border-top: 1px solid var(--border-light); }
.meta-item { display: flex; align-items: center; gap: 8px; font-size: 13px; }
.meta-icon { width: 16px; height: 16px; color: var(--text-secondary); }
.teacher-tag { color: var(--primary-color); font-weight: 600; background: var(--primary-soft); padding: 2px 8px; border-radius: 4px;}

.course-actions { display: flex; gap: 8px; padding: 0 24px 24px; }
.btn-action { 
  flex: 1; 
  display: inline-flex; 
  align-items: center; 
  justify-content: center; 
  gap: 6px; 
  padding: 12px; 
  border-radius: var(--border-radius-lg); 
  cursor: pointer; 
  border: 2px solid transparent;
  background: white;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}
.btn-action::before {
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
.btn-action:hover::before {
  opacity: 1;
}
.btn-action svg {
  width: 18px;
  height: 18px;
  transition: transform 0.3s;
}
.btn-action:hover svg {
  transform: scale(1.1);
}
.btn-action.collected { 
  background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
  border-color: #10b981; 
  color: white;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);
}
.btn-action.collected:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4);
}
.btn-primary { 
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%); 
  color: white; 
  border-color: var(--primary-color);
  box-shadow: 0 4px 14px rgba(13, 148, 136, 0.3);
}
.btn-primary:hover { 
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-color) 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(13, 148, 136, 0.4);
}

.fade-in { animation: fadeIn 0.4s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>