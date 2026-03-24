<template>
  <div class="page-container">
    <h2>资源浏览</h2>
    
    <div class="tab-section">
      <button 
        v-for="tab in tabs" 
        :key="tab.value"
        :class="['tab-btn', activeTab === tab.value ? 'active' : '']"
        @click="activeTab = tab.value"
      >
        {{ tab.label }}
      </button>
    </div>
    
    <div class="filter-section">
      <div class="search-box">
        <input v-model="searchText" :placeholder="getPlaceholder()" class="search-input" />
      </div>
      <div class="filter-box">
        <select v-model="filterType" class="filter-select">
          <option value="">全部类型</option>
          <option v-for="t in filteredTypes" :key="t.id" :value="t.id">{{ t.name }}</option>
        </select>
        <select v-model="sortBy" class="filter-select">
          <option value="downloads">下载最多</option>
          <option value="points">积分最低</option>
          <option value="newest">最新上传</option>
        </select>
      </div>
    </div>

    <div class="course-grid">
      <div v-for="course in filteredCourses" :key="course.id" class="course-card">
        <div class="course-header">
          <span class="course-type">{{ course.type_name || '未分类' }}</span>
          <span class="course-points">💎 {{ course.points_required }} 积分</span>
        </div>
        <h3 class="course-title">{{ course.title }}</h3>
        <p class="course-description">{{ course.description }}</p>
        <div class="course-meta">
          <span>👨‍🏫 {{ course.teacher?.name || course.teacher?.username }}</span>
          <span>📥 {{ course.downloads }} 次下载</span>
        </div>
        <div class="course-actions">
          <button @click="toggleCollect(course)" :class="['btn-collect', isCollected(course.id) ? 'collected' : '']">
            {{ isCollected(course.id) ? '★ 已收藏' : '☆ 收藏' }}
          </button>
          <button @click="viewDetails(course)" class="btn-view">查看详情</button>
          <button @click="downloadCourse(course)" class="btn-download">下载</button>
        </div>
      </div>
    </div>

    <div v-if="filteredCourses.length === 0" class="empty-state">
      <p>暂无课程数据</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const courses = ref<any[]>([])
const courseTypes = ref<any[]>([])
const collections = ref<any[]>([])
const searchText = ref('')
const filterType = ref('')
const sortBy = ref('downloads')
const activeTab = ref('online')

const tabs = [
  { label: '网络课程', value: 'online' },
  { label: '校内课程', value: 'campus' },
  { label: '书籍资源', value: 'books' }
]

const filteredTypes = computed(() => {
  if (activeTab.value === 'online') {
    // 网络课程类型：MOOC、哔哩哔哩
    return courseTypes.value.filter(type => type.name === 'MOOC' || type.name === '哔哩哔哩')
  } else if (activeTab.value === 'campus') {
    // 校内课程类型：人文类、海洋类、历史类、政治类
    return courseTypes.value.filter(type => 
      type.name === '人文类' || type.name === '海洋类' || type.name === '历史类' || type.name === '政治类'
    )
  } else if (activeTab.value === 'books') {
    // 书籍资源类型：二手书、电子书
    return courseTypes.value.filter(type => type.name === '二手书' || type.name === '电子书')
  }
  return courseTypes.value
})

const filteredCourses = computed(() => {
  let result = courses.value.filter(course => {
    const matchesSearch = course.title.toLowerCase().includes(searchText.value.toLowerCase()) ||
                         course.description.toLowerCase().includes(searchText.value.toLowerCase())
    const matchesType = !filterType.value || course.type === filterType.value
    
    // 根据标签页过滤
    let matchesTab = true
    if (activeTab.value === 'online') {
      // 网络课程：过滤出MOOC和哔哩哔哩类型
      matchesTab = course.type_name === 'MOOC' || course.type_name === '哔哩哔哩'
    } else if (activeTab.value === 'campus') {
      // 校内课程：过滤出校内老师上传的资源，且类型为人文类、海洋类、历史类、政治类
      matchesTab = course.teacher !== null && 
                   (course.type_name === '人文类' || course.type_name === '海洋类' || 
                    course.type_name === '历史类' || course.type_name === '政治类')
    } else if (activeTab.value === 'books') {
      // 书籍资源：过滤出书籍类型的资源
      matchesTab = course.type_name === '二手书' || course.type_name === '电子书'
    }
    
    return matchesSearch && matchesType && matchesTab
  })
  
  if (sortBy.value === 'downloads') {
    result.sort((a, b) => b.downloads - a.downloads)
  } else if (sortBy.value === 'points') {
    result.sort((a, b) => a.points_required - b.points_required)
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
    const response = await axios.get('http://127.0.0.1:8000/api/courses/')
    courses.value = response.data
  } catch (error) {
    console.error('获取课程列表失败', error)
  }
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
  alert(`课程详情:\n\n名称: ${course.title}\n类型: ${course.type_name}\n\n描述: ${course.description}\n\n所需积分: ${course.points_required}`)
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
  if (activeTab.value === 'online') {
    return '搜索网络课程...'
  } else if (activeTab.value === 'campus') {
    return '搜索校内课程...'
  } else {
    return '搜索书籍...'
  }
}

onMounted(() => {
  fetchCourseTypes()
  fetchCourses()
  fetchCollections()
})
</script>

<style scoped>
.page-container { padding: 20px; }
.tab-section { display: flex; gap: 10px; margin-bottom: 24px; border-bottom: 1px solid #eaeaea; }
.tab-btn { padding: 10px 20px; border: none; background: none; border-bottom: 2px solid transparent; cursor: pointer; font-size: 14px; font-weight: 500; color: #666; transition: all 0.3s; }
.tab-btn:hover { color: #409eff; }
.tab-btn.active { color: #409eff; border-bottom-color: #409eff; }
.filter-section { margin-bottom: 24px; }
.search-box { display: flex; gap: 10px; margin-bottom: 16px; }
.search-input { flex: 1; padding: 10px 16px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; }
.filter-box { display: flex; gap: 12px; }
.filter-select { padding: 10px 16px; border: 1px solid #ddd; border-radius: 6px; min-width: 150px; }

.course-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; }
.course-card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); transition: transform 0.2s; }
.course-card:hover { transform: translateY(-4px); }
.course-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.course-type { display: inline-block; padding: 4px 12px; background: #e6f7ff; color: #1890ff; border-radius: 4px; font-size: 12px; }
.course-points { color: #e6a23c; font-size: 14px; }
.course-title { font-size: 18px; font-weight: 600; margin: 0 0 8px; color: #333; }
.course-description { color: #666; font-size: 14px; margin: 0 0 16px; line-height: 1.6; }
.course-meta { display: flex; justify-content: space-between; color: #999; font-size: 13px; margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid #eee; }
.course-actions { display: flex; gap: 8px; }
.btn-collect, .btn-view, .btn-download { flex: 1; padding: 8px 12px; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; }
.btn-collect { background: #f0f9eb; color: #67c23a; }
.btn-collect.collected { background: #67c23a; color: white; }
.btn-view { background: #f4f4f5; color: #909399; }
.btn-download { background: #409eff; color: white; }

.empty-state { text-align: center; padding: 60px 20px; color: #999; }
</style>
