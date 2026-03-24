<template>
  <div class="page-container">
    <h2>个人中心</h2>
    
    <div class="profile-container">
      <div class="profile-card">
        <div class="profile-header">
          <div class="avatar">
            {{ user?.name?.charAt(0) || user?.username?.charAt(0) || '?' }}
          </div>
          <div class="user-info">
            <h3>{{ user?.name || user?.username }}</h3>
            <p class="role-tag">{{ getRoleText(user?.role) }}</p>
            <p class="points">积分: {{ user?.points || 0 }}</p>
          </div>
        </div>
        
        <div class="profile-details">
          <div class="detail-item">
            <span class="label">用户名</span>
            <span class="value">{{ user?.username }}</span>
          </div>
          <div class="detail-item" v-if="user?.role === 'student'">
            <span class="label">学号</span>
            <span class="value">{{ user?.student_id || '-' }}</span>
          </div>
          <div class="detail-item" v-if="user?.role === 'teacher'">
            <span class="label">工号</span>
            <span class="value">{{ user?.employee_id || '-' }}</span>
          </div>
          <div class="detail-item">
            <span class="label">姓名</span>
            <span class="value">{{ user?.name || '-' }}</span>
          </div>
        </div>
      </div>

      <div class="edit-card">
        <h3>编辑资料</h3>
        <form @submit.prevent="saveProfile" class="edit-form">
          <div class="form-group">
            <label>姓名</label>
            <input v-model="profileData.name" placeholder="请输入姓名" />
          </div>
          <div class="form-group">
            <label>邮箱</label>
            <input v-model="profileData.email" placeholder="请输入邮箱" type="email" />
          </div>
          <div class="form-group">
            <label>性别</label>
            <select v-model="profileData.gender">
              <option value="">请选择</option>
              <option value="male">男</option>
              <option value="female">女</option>
              <option value="other">其他</option>
            </select>
          </div>
          <div class="form-group">
            <label>手机号</label>
            <input v-model="profileData.phone" placeholder="请输入手机号" />
          </div>
          <div class="form-group">
            <label>个性签名</label>
            <textarea v-model="profileData.signature" placeholder="请输入个性签名" rows="2"></textarea>
          </div>
          <div class="form-group" v-if="user?.role === 'student'">
            <label>学号</label>
            <input v-model="profileData.student_id" placeholder="请输入学号" />
          </div>
          <div class="form-group" v-if="user?.role === 'student'">
            <label>专业</label>
            <input v-model="profileData.major" placeholder="请输入专业" />
          </div>
          <div class="form-group" v-if="user?.role === 'student'">
            <label>年级</label>
            <input v-model="profileData.grade" placeholder="请输入年级" />
          </div>
          <div class="form-group" v-if="user?.role === 'teacher'">
            <label>工号</label>
            <input v-model="profileData.employee_id" placeholder="请输入工号" />
          </div>
          <div class="form-group" v-if="user?.role === 'teacher'">
            <label>学科</label>
            <input v-model="profileData.subject" placeholder="请输入学科" />
          </div>
          <div class="form-group" v-if="user?.role === 'teacher'">
            <label>部门</label>
            <input v-model="profileData.department" placeholder="请输入部门" />
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-submit">保存修改</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref<any>(null)
const profileData = reactive({
  name: '',
  email: '',
  gender: '',
  phone: '',
  signature: '',
  student_id: '',
  employee_id: '',
  major: '',
  grade: '',
  subject: '',
  department: ''
})

const getRoleText = (role: string) => {
  const map: any = { admin: '管理员', student: '学生', teacher: '老师' }
  return map[role] || role
}

const fetchProfile = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/auth/profile/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    user.value = response.data
    Object.assign(profileData, {
      name: response.data.name || '',
      email: response.data.email || '',
      gender: response.data.gender || '',
      phone: response.data.phone || '',
      signature: response.data.signature || '',
      student_id: response.data.student_id || '',
      employee_id: response.data.employee_id || '',
      major: response.data.major || '',
      grade: response.data.grade || '',
      subject: response.data.subject || '',
      department: response.data.department || ''
    })
  } catch (error) {
    console.error('获取用户信息失败', error)
  }
}

const saveProfile = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.put('http://127.0.0.1:8000/api/auth/profile/', profileData, {
      headers: { Authorization: `Bearer ${token}` }
    })
    user.value = response.data
    localStorage.setItem('user', JSON.stringify(response.data))
    alert('保存成功')
  } catch (error) {
    alert('保存失败')
  }
}

onMounted(() => {
  const storedUser = localStorage.getItem('user')
  if (storedUser) {
    user.value = JSON.parse(storedUser)
  }
  fetchProfile()
})
</script>

<style scoped>
.page-container { padding: 20px; }
.profile-container { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.profile-card, .edit-card { background: white; padding: 24px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.profile-header { display: flex; gap: 20px; margin-bottom: 24px; padding-bottom: 24px; border-bottom: 1px solid #eee; }
.avatar { width: 80px; height: 80px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 32px; color: white; font-weight: bold; }
.user-info { flex: 1; }
.user-info h3 { margin: 0 0 8px; color: #333; }
.role-tag { display: inline-block; padding: 4px 12px; background: #e6f7ff; color: #1890ff; border-radius: 4px; font-size: 12px; margin-bottom: 8px; }
.points { color: #e6a23c; font-weight: bold; margin: 0; }
.profile-details { display: flex; flex-direction: column; gap: 12px; }
.detail-item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f5f5f5; }
.label { color: #999; }
.value { color: #333; font-weight: 500; }
.edit-card h3 { margin: 0 0 20px; color: #333; border-bottom: 2px solid #409eff; padding-bottom: 10px; }
.edit-form { display: flex; flex-direction: column; gap: 16px; }
.form-group { display: flex; flex-direction: column; gap: 8px; }
.form-group label { color: #666; font-weight: 500; }
.form-group input, .form-group textarea, .form-group select { padding: 10px 12px; border: 1px solid #ddd; border-radius: 4px; }
.form-actions { padding-top: 10px; }
.btn-submit { padding: 10px 24px; background: #409eff; color: white; border: none; border-radius: 4px; cursor: pointer; }
.btn-submit:hover { background: #66b1ff; }
</style>
