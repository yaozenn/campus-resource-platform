<template>
  <div class="page-container">
    <h2>公告</h2>
    <div class="announcement-list">
      <div v-for="ann in announcements" :key="ann.id" class="announcement-item">
        <h3>{{ ann.title }}</h3>
        <p>{{ ann.content }}</p>
        <div class="announcement-info">
          <span>发布者: {{ ann.author?.name || ann.author?.username }}</span>
          <span>时间: {{ ann.publish_date }}</span>
          <span class="visible-tag">{{ getVisibleText(ann.visible_to) }}</span>
        </div>
      </div>
    </div>
    <div v-if="announcements.length === 0" class="empty-state">
      <p>暂无公告</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const announcements = ref<any[]>([])

const getVisibleText = (visible: string) => {
  const map: any = { all: '公开', student: '学生', teacher: '老师' }
  return map[visible] || visible
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
.page-container { padding: 20px; }
.announcement-list { display: flex; flex-direction: column; gap: 15px; }
.announcement-item { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 4px solid #409eff; }
.announcement-item h3 { margin: 0 0 10px; }
.announcement-item p { color: #666; line-height: 1.6; }
.announcement-info { display: flex; justify-content: space-between; color: #999; font-size: 14px; margin-top: 10px; }
.visible-tag { background: #e6f7ff; color: #1890ff; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.empty-state { text-align: center; padding: 60px 20px; color: #999; }
</style>
