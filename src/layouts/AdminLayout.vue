<template>
  <div class="dashboard">
    <!-- 顶部导航栏 - 磨玻璃效果 -->
    <header class="top-nav glass">
      <div class="nav-brand">
        <IconSettings class="brand-icon" />
        <span class="brand-name">管理后台</span>
      </div>
      
      <nav class="nav-menu">
        <router-link to="/admin/teachers" class="nav-item">
          <IconUser class="nav-icon" />
          <span>老师管理</span>
        </router-link>
        <router-link to="/admin/students" class="nav-item">
          <IconUser class="nav-icon" />
          <span>学生管理</span>
        </router-link>
        <router-link to="/admin/resources" class="nav-item">
          <IconBook class="nav-icon" />
          <span>资源管理</span>
        </router-link>
        <router-link to="/admin/forum" class="nav-item">
          <IconForum class="nav-icon" />
          <span>论坛管理</span>
        </router-link>
        <router-link to="/admin/announcements" class="nav-item">
          <IconAnnouncement class="nav-icon" />
          <span>公告管理</span>
        </router-link>
        <router-link to="/admin/analysis" class="nav-item">
          <IconCollection class="nav-icon" />
          <span>数据分析</span>
        </router-link>
        <router-link to="/admin/points" class="nav-item">
          <IconStar class="nav-icon" />
          <span>积分管理</span>
        </router-link>
      </nav>
      
      <div class="nav-actions">
        <router-link to="/admin/personal" class="user-info">
          <img v-if="userAvatar" :src="userAvatar" alt="头像" class="user-avatar-img" />
          <div v-else class="user-avatar">{{ userInitial }}</div>
          <span class="user-name">{{ userName }}</span>
        </router-link>
        <button @click="handleLogout" class="logout-btn" title="退出登录">
          <IconLogout class="logout-icon" />
        </button>
      </div>
    </header>
    
    <!-- 主内容区 -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  IconSettings, 
  IconUsers, 
  IconBook, 
  IconStar, 
  IconMessage, 
  IconAnnouncement, 
  IconDatabase, 
  IconLogout,
  IconSparkles,
  IconFile,
  IconPlus,
  IconUser,
  IconForum,
  IconCollection
} from '../components/icons'
import { getAvatar, getUserInitial, getUserName } from '../utils/avatar'

const router = useRouter()
const userAvatar = ref(getAvatar())
const userName = computed(() => getUserName())
const userInitial = computed(() => getUserInitial())

// 监听localStorage变化，实时更新头像
const handleStorageChange = () => {
  userAvatar.value = getAvatar()
}

// 监听localStorage变化
window.addEventListener('storage', handleStorageChange)

// 组件卸载时移除监听器
onUnmounted(() => {
  window.removeEventListener('storage', handleStorageChange)
})

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: var(--bg-color);
}

/* 顶部导航栏 - 磨玻璃效果 */
.top-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  z-index: 1000;
  border-bottom: 1px solid var(--glass-border);
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-icon {
  width: 32px;
  height: 32px;
  color: var(--primary-color);
}

.brand-name {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  font-family: var(--font-sf);
  letter-spacing: -0.5px;
}

/* 导航菜单 */
.nav-menu {
  display: flex;
  align-items: center;
  gap: 2px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: var(--border-radius-md);
  font-size: 13px;
  font-weight: 500;
  transition: all var(--transition-fast);
}

.nav-item:hover {
  color: var(--primary-color);
  background: rgba(13, 148, 136, 0.08);
}

.nav-item.router-link-active {
  color: var(--primary-color);
  background: rgba(13, 148, 136, 0.12);
}

.nav-icon {
  width: 16px;
  height: 16px;
}

/* 右侧操作区 */
.nav-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  padding: 6px 12px 6px 6px;
  border-radius: 24px;
  transition: background var(--transition-fast);
}

.user-info:hover {
  background: rgba(13, 148, 136, 0.08);
}

.user-avatar {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #ef4444, #f97316);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  color: white;
}

.user-avatar-img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.logout-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: 50%;
  cursor: pointer;
  color: var(--text-secondary);
  transition: all var(--transition-fast);
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.1);
  border-color: #ef4444;
  color: #ef4444;
}

.logout-icon {
  width: 20px;
  height: 20px;
}

/* 主内容区 */
.main-content {
  padding-top: 64px;
  min-height: 100vh;
}
</style>
