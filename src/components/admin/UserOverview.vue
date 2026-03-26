<template>
  <div class="page-container">
    <div class="page-header">
      <button @click="goBack" class="btn-back">
        <IconArrowLeft class="btn-icon" />
        返回数据分析
      </button>
      <h2>
        <IconUsers class="header-icon" />
        用户总览
      </h2>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-summary">
      <div class="summary-card">
        <div class="summary-icon"><IconUsers class="icon-svg" /></div>
        <div class="summary-value">{{ totalUsers }}</div>
        <div class="summary-label">总用户数</div>
      </div>
      <div class="summary-card">
        <div class="summary-icon"><IconUser class="icon-svg" /></div>
        <div class="summary-value">{{ teacherCount }}</div>
        <div class="summary-label">老师</div>
      </div>
      <div class="summary-card">
        <div class="summary-icon"><IconUserCircle class="icon-svg" /></div>
        <div class="summary-value">{{ studentCount }}</div>
        <div class="summary-label">学生</div>
      </div>
      <div class="summary-card">
        <div class="summary-icon"><IconSettings class="icon-svg" /></div>
        <div class="summary-value">{{ adminCount }}</div>
        <div class="summary-label">管理员</div>
      </div>
      <div class="summary-card">
        <div class="summary-icon"><IconUser class="icon-svg" /></div>
        <div class="summary-value">{{ maleCount }}</div>
        <div class="summary-label">男性</div>
      </div>
      <div class="summary-card">
        <div class="summary-icon"><IconUser class="icon-svg" /></div>
        <div class="summary-value">{{ femaleCount }}</div>
        <div class="summary-label">女性</div>
      </div>
    </div>

    <!-- 用户列表 -->
    <div class="user-section">
      <h3>用户列表</h3>
      <div class="filter-bar">
        <input v-model="searchText" placeholder="搜索用户名..." class="search-input" />
        <select v-model="filterRole" class="filter-select">
          <option value="">全部角色</option>
          <option value="admin">管理员</option>
          <option value="teacher">老师</option>
          <option value="student">学生</option>
        </select>
      </div>
      
      <div class="user-list">
        <div v-for="user in filteredUsers" :key="user.id" class="user-card">
          <div class="user-avatar">{{ user.name.charAt(0) }}</div>
          <div class="user-info">
            <div class="user-name">{{ user.name }}</div>
            <div class="user-username">@{{ user.username }}</div>
            <div class="user-meta">
              <span class="role-tag" :class="user.role">{{ getRoleText(user.role) }}</span>
              <span v-if="user.gender"><IconUser class="meta-icon-svg" /> {{ user.gender }}</span>
              <span v-if="user.major"><IconBookOpen class="meta-icon-svg" /> {{ user.major }}</span>
              <span v-if="user.grade"><IconGraduationCap class="meta-icon-svg" /> {{ user.grade }}级</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { IconUsers, IconUser, IconUserCircle, IconSettings, IconArrowLeft, IconBookOpen, IconGraduationCap } from '../icons'

const router = useRouter()
const users = ref<any[]>([])
const searchText = ref('')
const filterRole = ref('')

const totalUsers = computed(() => users.value.length)
const teacherCount = computed(() => users.value.filter(u => u.role === 'teacher').length)
const studentCount = computed(() => users.value.filter(u => u.role === 'student').length)
const adminCount = computed(() => users.value.filter(u => u.role === 'admin').length)
const maleCount = computed(() => users.value.filter(u => u.gender === '男' || u.gender === 'male').length)
const femaleCount = computed(() => users.value.filter(u => u.gender === '女' || u.gender === 'female').length)

const filteredUsers = computed(() => {
  return users.value.filter(user => {
    const matchSearch = searchText.value === '' || 
                       user.name.includes(searchText.value) ||
                       user.username.includes(searchText.value)
    const matchRole = filterRole.value === '' || user.role === filterRole.value
    return matchSearch && matchRole
  })
})

const getRoleText = (role: string) => {
  const map: any = { admin: '管理员', teacher: '老师', student: '学生' }
  return map[role] || role
}

const fetchUsers = async () => {
  try {
    const token = localStorage.getItem('token')
    // 尝试使用 users API，如果不存在则使用 students + teachers
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/auth/students/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      const students = response.data
      
      const response2 = await axios.get('http://127.0.0.1:8000/api/auth/teachers/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      const teachers = response2.data
      
      const response3 = await axios.get('http://127.0.0.1:8000/api/auth/profile/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      const admins = [response3.data].filter(u => u.role === 'admin')
      
      users.value = [...students, ...teachers, ...admins]
    } catch (e) {
      // 如果 API 不存在，使用备用方案
      const response = await axios.get('http://127.0.0.1:8000/api/stats/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (response.data.success) {
        // 从统计数据中获取用户分布
        userDistribution.value = response.data.userDistribution
      }
      users.value = []
    }
  } catch (error) {
    console.error('获取用户列表失败', error)
  }
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.page-container { padding: var(--spacing-lg); }

.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: var(--spacing-lg);
}

.btn-back {
  padding: 10px 20px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  cursor: pointer;
  font-size: var(--font-size-base);
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all var(--transition-fast);
}

.btn-back:hover {
  background: var(--bg-tertiary);
  border-color: var(--primary-color);
}

.btn-icon { width: 16px; height: 16px; }

.page-header h2 {
  margin: 0;
  color: var(--text-primary);
  font-size: var(--h2-font-size);
  font-weight: var(--h2-font-weight);
  display: flex;
  align-items: center;
}

.header-icon { width: 28px; height: 28px; color: var(--primary-color); margin-right: 10px; }

.stats-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.summary-card {
  background: var(--bg-primary);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  text-align: center;
  transition: box-shadow var(--transition-normal);
}

.summary-card:hover { box-shadow: var(--shadow-md); }

.summary-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto var(--spacing-sm);
  background: rgba(13, 148, 136, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-svg { width: 24px; height: 24px; color: var(--primary-color); }

.summary-value {
  font-size: 32px;
  font-weight: var(--font-weight-bold);
  color: var(--primary-color);
  margin-bottom: 8px;
}

.summary-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.user-section h3 {
  margin-bottom: var(--spacing-md);
  color: var(--text-primary);
  font-size: var(--h4-font-size);
  font-weight: var(--h4-font-weight);
}

.filter-bar {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.search-input, .filter-select {
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-base);
  background: var(--bg-primary);
  transition: border-color var(--transition-fast);
}

.search-input:focus, .filter-select:focus {
  outline: none;
  border-color: var(--primary-color);
}

.search-input {
  flex: 1;
}

.filter-select {
  min-width: 150px;
}

.user-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.user-card {
  display: flex;
  align-items: center;
  gap: 20px;
  background: var(--bg-primary);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  transition: box-shadow var(--transition-normal);
}

.user-card:hover { box-shadow: var(--shadow-md); }

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: var(--font-weight-bold);
  flex-shrink: 0;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin-bottom: 5px;
}

.user-username {
  font-size: var(--font-size-sm);
  color: var(--text-tertiary);
  margin-bottom: 10px;
}

.user-meta {
  display: flex;
  gap: 15px;
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.user-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.meta-icon-svg { width: 14px; height: 14px; }

.role-tag {
  padding: 4px 12px;
  border-radius: var(--border-radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
}

.role-tag.admin {
  background: rgba(239, 68, 68, 0.1);
  color: var(--danger-color);
}

.role-tag.teacher {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.role-tag.student {
  background: rgba(16, 185, 129, 0.1);
  color: var(--success-color);
}
</style>
