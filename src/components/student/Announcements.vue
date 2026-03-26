<template>
  <div class="page-container">
    <h2>
      <IconBell class="header-icon" />
      公告
    </h2>
    <div class="announcement-list">
      <div 
        v-for="ann in announcements" 
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
    <div v-if="announcements.length === 0" class="empty-state">
      <IconInbox class="empty-icon" />
      <p>暂无公告</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { formatDateTime } from '../../utils/timeFormat'
import { IconBell, IconUser, IconCalendar, IconInbox } from '@/components/icons'

const router = useRouter()
const announcements = ref<any[]>([])

const getVisibleText = (visible: string) => {
  const map: any = { all: '公开', student: '学生', teacher: '老师' }
  return map[visible] || visible
}

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
  try {
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    const response = await axios.get(`http://127.0.0.1:8000/api/announcements/?role=${user.role}`)
    announcements.value = response.data
  } catch (error) {
    console.error('获取公告失败', error)
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
