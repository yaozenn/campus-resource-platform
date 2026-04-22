<template>
  <div class="dashboard">
    <header class="top-nav glass">
      <div class="nav-brand">
        <IconBook class="brand-icon" />
        <span class="brand-name">校园课程资源共享平台</span>
      </div>
      
      <nav class="nav-menu">
        <router-link to="/student/courses" class="nav-item">
          <IconBook class="nav-icon" />
          <span>大厅浏览</span>
        </router-link>
        <router-link to="/student/uploads" class="nav-item">
          <IconUpload class="nav-icon" />
          <span>我的分享</span>
        </router-link>
        <router-link to="/student/collections" class="nav-item">
          <IconStar class="nav-icon" />
          <span>收藏</span>
        </router-link>
        <router-link to="/student/forum" class="nav-item">
          <IconForum class="nav-icon" />
          <span>论坛</span>
        </router-link>
        <router-link to="/student/announcements" class="nav-item">
          <IconAnnouncement class="nav-icon" />
          <span>公告</span>
        </router-link>
      </nav>
      
      <div class="nav-actions">
        <div class="user-points-badge" @click="goToPoints">
          <IconStar class="points-icon" />
          <span>{{ userPoints }} 积分</span>
        </div>
        <router-link to="/student/personal" class="user-avatar-link">
          <img v-if="userAvatar" :src="userAvatar" alt="头像" class="user-avatar-img" />
          <div v-else class="user-avatar">{{ userInitial }}</div>
        </router-link>
        <button @click="handleLogout" class="logout-btn" title="退出登录">
          <IconLogout class="logout-icon" />
        </button>
      </div>
    </header>
    
    <main class="main-content">
      <router-view />
    </main>
    
    <AIAssistantFloating />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import AIAssistantFloating from '../components/student/AIAssistantFloating.vue'
import { 
  IconBook, 
  IconStar, 
  IconForum, 
  IconAnnouncement, 
  IconLogout,
  IconUser,
  IconMessage,
  IconUpload
} from '../components/icons'

const router = useRouter()
const user = JSON.parse(localStorage.getItem('user') || '{}')
const userAvatar = user.avatar || ''
const userName = computed(() => user.name || user.username || '同学')
const userInitial = computed(() => (user.name || user.username || 'S').charAt(0).toUpperCase())
const userPoints = computed(() => user.points || 0)

const goToPoints = () => {
  router.push('/student/points')
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.dashboard { min-height: 100vh; background: var(--bg-color); }
.top-nav { position: fixed; top: 0; left: 0; right: 0; height: 64px; display: flex; align-items: center; justify-content: space-between; padding: 0 32px; z-index: 1000; border-bottom: 1px solid var(--glass-border); }
.nav-brand { display: flex; align-items: center; gap: 12px; }
.brand-icon { width: 32px; height: 32px; color: var(--primary-color); }
.brand-name { font-size: 20px; font-weight: 700; color: var(--text-primary); font-family: var(--font-sf); letter-spacing: -0.5px; }
.nav-menu { display: flex; align-items: center; gap: 8px; }
.nav-item { display: flex; align-items: center; gap: 8px; padding: 10px 20px; color: var(--text-secondary); text-decoration: none; border-radius: var(--border-radius-md); font-size: 15px; font-weight: 500; transition: all var(--transition-fast); }
.nav-item:hover { color: var(--primary-color); background: rgba(13, 148, 136, 0.08); }
.nav-item.router-link-active { color: var(--primary-color); background: rgba(13, 148, 136, 0.12); }
.nav-icon { width: 20px; height: 20px; }
.nav-actions { display: flex; align-items: center; gap: 16px; }
.user-points-badge { display: flex; align-items: center; gap: 6px; padding: 6px 14px; background: linear-gradient(135deg, #f59e0b, #fbbf24); color: white; border-radius: 20px; font-size: 14px; font-weight: 600; text-decoration: none; transition: all var(--transition-fast); cursor: pointer; }
.user-points-badge:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4); }
.points-icon { width: 16px; height: 16px; color: white; }
.user-avatar-link { text-decoration: none; }
.user-avatar { width: 40px; height: 40px; background: linear-gradient(135deg, var(--primary-color), var(--primary-light)); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: 700; color: white; transition: transform var(--transition-fast); }
.user-avatar:hover { transform: scale(1.05); }
.user-avatar-img { width: 40px; height: 40px; border-radius: 50%; object-fit: cover; transition: transform var(--transition-fast); }
.user-avatar-img:hover { transform: scale(1.05); }
.logout-btn { width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; background: transparent; border: 1px solid var(--border-color); border-radius: 50%; cursor: pointer; color: var(--text-secondary); transition: all var(--transition-fast); }
.logout-btn:hover { background: rgba(239, 68, 68, 0.1); border-color: #ef4444; color: #ef4444; }
.logout-icon { width: 20px; height: 20px; }
.main-content { padding-top: 64px; min-height: 100vh; }
</style>