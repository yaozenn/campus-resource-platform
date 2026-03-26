<template>
  <div class="page-container">
    <h2>学生管理</h2>
    <div class="stats-bar">
      <div class="stat-item">
        <div class="stat-value">{{ students.length }}</div>
        <div class="stat-label">我的学生</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{{ getMajorCount }}</div>
        <div class="stat-label">专业分布</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{{ getGradeCount }}</div>
        <div class="stat-label">年级分布</div>
      </div>
    </div>

    <div class="filter-bar">
      <input
        v-model="searchText"
        placeholder="搜索学生姓名或学号..."
        class="search-input"
      />
      <select v-model="filterMajor" class="filter-select">
        <option value="">所有专业</option>
        <option v-for="major in majors" :key="major" :value="major">{{ major }}</option>
      </select>
      <select v-model="filterGrade" class="filter-select">
        <option value="">所有年级</option>
        <option v-for="grade in grades" :key="grade" :value="grade">{{ grade }}级</option>
      </select>
    </div>

    <div class="student-list">
      <div v-for="student in filteredStudents" :key="student.id" class="student-card">
        <div class="student-avatar">
          <div class="avatar-placeholder">{{ student.name.charAt(0) }}</div>
        </div>
        <div class="student-info">
          <h3>{{ student.name }}</h3>
          <p class="student-username">@{{ student.username }}</p>
          <div class="student-details">
            <span class="tag">{{ getGenderText(student.gender) }}</span>
            <span class="tag tag-primary">{{ student.major }}</span>
            <span class="tag tag-success">{{ student.grade }}级</span>
          </div>
          <div class="student-meta">
            <span class="meta-item">
              <IconEmail class="meta-icon" />
              {{ student.email }}
            </span>
            <span class="meta-item">
              <IconPhone class="meta-icon" />
              {{ student.phone || '未设置' }}
            </span>
          </div>
        </div>
        <div class="student-actions">
          <button @click="viewStudent(student)" class="btn-view">查看详情</button>
        </div>
      </div>

      <div v-if="filteredStudents.length === 0" class="empty-state">
        <IconUser class="empty-icon" />
        <p>暂无学生</p>
      </div>
    </div>

    <!-- 学生详情弹窗 -->
    <div v-if="showDetailDialog" class="dialog-overlay" @click="closeDetailDialog">
      <div class="dialog-content" @click.stop>
        <div class="dialog-header">
          <h3>学生详情</h3>
          <button class="btn-close" @click="closeDetailDialog">
            <IconClose class="close-icon" />
          </button>
        </div>
        <div v-if="selectedStudent" class="dialog-body">
          <div class="detail-avatar">
            {{ selectedStudent.name.charAt(0) }}
          </div>
          <div class="detail-name">{{ selectedStudent.name }}</div>
          <div class="detail-username">@{{ selectedStudent.username }}</div>
          
          <div class="detail-grid">
            <div class="detail-item">
              <span class="detail-label"><IconUser class="detail-icon" /> 性别</span>
              <span class="detail-value">{{ getGenderText(selectedStudent.gender) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label"><IconBookOpen class="detail-icon" /> 专业</span>
              <span class="detail-value">{{ selectedStudent.major || '未设置' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label"><IconGraduationCap class="detail-icon" /> 年级</span>
              <span class="detail-value">{{ selectedStudent.grade }}级</span>
            </div>
            <div class="detail-item">
              <span class="detail-label"><IconEmail class="detail-icon" /> 邮箱</span>
              <span class="detail-value">{{ selectedStudent.email || '未设置' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label"><IconPhone class="detail-icon" /> 电话</span>
              <span class="detail-value">{{ selectedStudent.phone || '未设置' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label"><IconCalendar class="detail-icon" /> 注册时间</span>
              <span class="detail-value">{{ selectedStudent.date_joined ? formatDateTime(selectedStudent.date_joined) : '未知' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { IconEmail, IconPhone, IconUser, IconClose, IconBookOpen, IconGraduationCap, IconCalendar } from '../../components/icons'
import { formatDateTime } from '../../utils/timeFormat'

const students = ref<any[]>([])
const searchText = ref('')
const filterMajor = ref('')
const filterGrade = ref('')

const currentUser = computed(() => {
  return JSON.parse(localStorage.getItem('user') || '{}')
})

const majors = computed(() => {
  const set = new Set(students.value.map(s => s.major))
  return Array.from(set)
})

const grades = computed(() => {
  const set = new Set(students.value.map(s => s.grade))
  return Array.from(set)
})

const getMajorCount = computed(() => majors.value.length)
const getGradeCount = computed(() => grades.value.length)

const filteredStudents = computed(() => {
  return students.value.filter(student => {
    const matchesSearch = searchText.value === '' ||
                         student.name.includes(searchText.value) ||
                         student.username.includes(searchText.value)
    const matchesMajor = filterMajor.value === '' || student.major === filterMajor.value
    const matchesGrade = filterGrade.value === '' || student.grade === filterGrade.value
    return matchesSearch && matchesMajor && matchesGrade
  })
})

const getGenderText = (gender: string) => {
  const map: any = { male: '男', female: '女', other: '其他' }
  return map[gender] || '未知'
}

const fetchStudents = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/auth/students/', {
      headers: { Authorization: `Bearer ${token}` },
      params: { supervisor_id: currentUser.value.id }
    })
    students.value = response.data
  } catch (error) {
    console.error('获取学生列表失败', error)
    // 如果 API 不支持过滤，就在前端过滤
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/auth/students/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      // 过滤出当前老师的学生
      students.value = response.data.filter((s: any) => s.supervisor === currentUser.value.id)
    } catch (error) {
      console.error('获取学生列表失败', error)
    }
  }
}

const selectedStudent = ref<any>(null)
const showDetailDialog = ref(false)

const viewStudent = (student: any) => {
  selectedStudent.value = student
  showDetailDialog.value = true
}

const closeDetailDialog = () => {
  showDetailDialog.value = false
  selectedStudent.value = null
}

onMounted(() => {
  fetchStudents()
})
</script>

<style scoped>
.page-container { padding: 20px; }

h2 { margin-bottom: 20px; color: var(--text-primary); font-family: var(--font-sf); }

.stats-bar {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}

.stat-item {
  flex: 1;
  background: white;
  padding: 20px;
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  text-align: center;
  border: 1px solid var(--border-light);
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: 8px;
  font-family: var(--font-sf);
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.filter-bar {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.search-input, .filter-select {
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: 14px;
  transition: all var(--transition-fast);
}

.search-input:focus, .filter-select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
}

.search-input {
  flex: 1;
}

.filter-select {
  min-width: 150px;
}

.student-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.student-card {
  display: flex;
  align-items: center;
  gap: 20px;
  background: white;
  padding: 20px;
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  transition: all var(--transition-fast);
  border: 1px solid var(--border-light);
}

.student-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.student-avatar {
  flex-shrink: 0;
}

.avatar-placeholder {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 700;
}

.student-info {
  flex: 1;
}

.student-info h3 {
  margin: 0 0 5px;
  color: var(--text-primary);
  font-size: 18px;
  font-weight: 600;
}

.student-username {
  margin: 0 0 10px;
  color: var(--text-tertiary);
  font-size: 14px;
}

.student-details {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}

.tag {
  padding: 4px 12px;
  background: var(--bg-tertiary);
  border-radius: 12px;
  font-size: 12px;
  color: var(--text-secondary);
}

.tag-primary {
  background: rgba(13, 148, 136, 0.1);
  color: var(--primary-color);
}

.tag-success {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.student-meta {
  display: flex;
  gap: 20px;
  font-size: 14px;
  color: var(--text-secondary);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.meta-icon {
  width: 16px;
  height: 16px;
  color: var(--text-tertiary);
}

.student-actions {
  flex-shrink: 0;
}

.btn-view {
  padding: 10px 24px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-weight: 500;
}

.btn-view:hover {
  background: var(--primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3);
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-placeholder);
}

.empty-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  color: var(--text-tertiary);
}

/* 详情弹窗样式 */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog-content {
  background: var(--bg-primary);
  border-radius: var(--border-radius-lg);
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border-light);
}

.dialog-header h3 {
  margin: 0;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.btn-close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  color: var(--text-tertiary);
  transition: color var(--transition-fast);
}

.btn-close:hover {
  color: var(--text-primary);
}

.close-icon {
  width: 24px;
  height: 24px;
}

.dialog-body {
  padding: var(--spacing-xl);
  text-align: center;
}

.detail-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: 700;
  margin: 0 auto var(--spacing-md);
}

.detail-name {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin-bottom: 4px;
}

.detail-username {
  font-size: var(--font-size-sm);
  color: var(--text-tertiary);
  margin-bottom: var(--spacing-lg);
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
  text-align: left;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: var(--spacing-md);
  background: var(--bg-secondary);
  border-radius: var(--border-radius-md);
}

.detail-label {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  gap: 4px;
}

.detail-icon {
  width: 14px;
  height: 14px;
}

.detail-value {
  font-size: var(--font-size-sm);
  color: var(--text-primary);
  font-weight: var(--font-weight-medium);
}

@media (max-width: 480px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
