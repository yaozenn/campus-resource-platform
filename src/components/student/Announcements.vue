<template>
  <div class="page-container">
    <h2>
      <IconBell class="header-icon" />
      公告
    </h2>
    <div class="search-bar">
      <IconSearch class="search-icon" />
      <input
        v-model="searchText"
        placeholder="搜索公告..."
        class="search-input"
      />
      <button v-if="searchText" @click="searchText = ''" class="clear-btn">
        <IconClose class="clear-icon" />
      </button>
    </div>
    <div class="announcement-list">
      <div 
        v-for="ann in filteredAnnouncements" 
        :key="ann.id" 
        class="announcement-item"
        @click="viewAnnouncement(ann)"
      >
        <h3>{{ ann.title }}</h3>
        <p>{{ ann.content.substring(0, 100) }}{{ ann.content.length > 100 ? '...' : '' }}</p>
        <div class="announcement-info">
          <span><IconUser class="info-icon" /> {{ ann.author?.name || ann.author?.username }}</span>
          <span><IconCalendar class="info-icon" /> {{ formatDateTime(ann.publish_date) }}</span>
          <span class="visible-tag">{{ getVisibleText(ann.visible_to) }}</span>
        </div>
      </div>
    </div>
    <div v-if="filteredAnnouncements.length === 0 && !loading" class="empty-state">
      <IconInbox class="empty-icon" />
      <p>{{ searchText ? '未找到匹配的公告' : '暂无公告' }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { formatDateTime } from '../../utils/timeFormat'
import { IconBell, IconUser, IconCalendar, IconInbox, IconSearch, IconClose } from '@/components/icons'

const router = useRouter()
const announcements = ref<any[]>([])
const searchText = ref('')
const loading = ref(true)

const getVisibleText = (visible: string) => {
  const map: any = { all: '公开', student: '学生', teacher: '老师' }
  return map[visible] || visible
}

const filteredAnnouncements = computed(() => {
  if (!searchText.value) {
    return announcements.value
  }
  const search = searchText.value.toLowerCase()
  return announcements.value.filter(ann => 
    ann.title.toLowerCase().includes(search) || 
    ann.content.toLowerCase().includes(search)
  )
})

const viewAnnouncement = (ann: any) => {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  if (user.role === 'teacher') {
    router.push(`/teacher/announcements/${ann.id}`)
  } else if (user.role === 'admin') {
    router.push(`/admin/announcements/${ann.id}`)
  } else {
    router.push(`/student/announcements/${ann.id}`)
  }
}

const fetchAnnouncements = async () => {
  loading.value = true
  try {
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    const response = await axios.get(`http://127.0.0.1:8000/api/announcements/?role=${user.role}`)
    announcements.value = response.data
  } catch (error) {
    console.error('获取公告失败', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchAnnouncements()
})
</script>

<style scoped>
.page-container { padding: var(--spacing-lg); }
.page-container h2 { margin: 0 0 var(--spacing-lg); font-size: var(--h2-font-size); font-weight: var(--h2-font-weight); color: var(--text-primary); display: flex; align-items: center; }
.header-icon { width: 28px; height: 28px; color: var(--primary-color); margin-right: 10px; }

.search-bar {
  position: relative;
  display: flex;
  align-items: center;
  margin-bottom: var(--spacing-lg);
  background: var(--bg-primary);
  border: 2px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  padding: 0 16px;
  transition: all 0.2s;
}
.search-bar:focus-within {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
}
.search-icon {
  width: 20px;
  height: 20px;
  color: var(--text-placeholder);
  flex-shrink: 0;
}
.search-input {
  flex: 1;
  padding: 14px 12px;
  border: none;
  background: transparent;
  font-size: 15px;
  outline: none;
  color: var(--text-primary);
}
.search-input::placeholder {
  color: var(--text-placeholder);
}
.clear-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  background: var(--bg-secondary);
  border-radius: 50%;
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.2s;
}
.clear-btn:hover {
  background: var(--border-color);
}
.clear-icon {
  width: 16px;
  height: 16px;
  color: var(--text-secondary);
}

.announcement-list { display: flex; flex-direction: column; gap: var(--spacing-md); }
.announcement-item { background: var(--bg-primary); padding: var(--spacing-lg); border-radius: var(--border-radius-lg); box-shadow: var(--shadow-sm); border-left: 4px solid var(--primary-color); transition: box-shadow var(--transition-normal); cursor: pointer; }
.announcement-item:hover { box-shadow: var(--shadow-md); }
.announcement-item h3 { margin: 0 0 var(--spacing-sm); color: var(--text-primary); font-size: var(--font-size-lg); font-weight: var(--font-weight-semibold); }
.announcement-item p { color: var(--text-secondary); line-height: 1.6; }
.announcement-info { display: flex; justify-content: space-between; align-items: center; color: var(--text-tertiary); font-size: var(--font-size-sm); margin-top: var(--spacing-sm); }
.announcement-info span { display: flex; align-items: center; gap: 4px; }
.info-icon { width: 14px; height: 14px; }
.visible-tag { background: rgba(13, 148, 136, 0.1); color: var(--primary-color); padding: 4px 12px; border-radius: var(--border-radius-full); font-size: var(--font-size-xs); font-weight: var(--font-weight-medium); }
.empty-state { text-align: center; padding: 60px 20px; color: var(--text-tertiary); }
.empty-icon { width: 64px; height: 64px; margin-bottom: var(--spacing-md); }
</style>
