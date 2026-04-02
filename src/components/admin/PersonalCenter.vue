<template>
  <div class="page-container">
    <div class="page-header">
      <h2>个人中心</h2>
      <p class="subtitle">管理系统超级管理员配置信息</p>
    </div>
    
    <div class="profile-container fade-in">
      <div class="profile-card card">
        <div class="profile-header">
          <div class="avatar-gradient">
            {{ user?.name?.charAt(0) || user?.username?.charAt(0) || 'A' }}
          </div>
          <div class="user-info">
            <h3>{{ user?.name || user?.username }}</h3>
            <span class="role-tag">{{ getRoleText(user?.role) }}</span>
          </div>
        </div>
        
        <div class="profile-details">
          <div class="detail-item">
            <span class="label">登录账号</span>
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
            <span class="label">真实姓名</span>
            <span class="value">{{ user?.name || '-' }}</span>
          </div>
        </div>
      </div>

      <div class="edit-card card">
        <div class="card-header">
          <h3>编辑资料</h3>
        </div>
        <div class="card-body">
          <form @submit.prevent="saveProfile" class="edit-form">
            <div class="form-grid">
              <div class="form-group">
                <label>姓名</label>
                <input v-model="profileData.name" placeholder="请输入姓名" class="input" />
              </div>
              <div class="form-group">
                <label>邮箱</label>
                <input v-model="profileData.email" placeholder="请输入邮箱" type="email" class="input" />
              </div>
              <div class="form-group">
                <label>性别</label>
                <select v-model="profileData.gender" class="input">
                  <option value="">请选择</option>
                  <option value="male">男</option>
                  <option value="female">女</option>
                  <option value="other">其他</option>
                </select>
              </div>
              <div class="form-group">
                <label>手机号</label>
                <input v-model="profileData.phone" placeholder="请输入手机号" class="input" />
              </div>
              
              <template v-if="user?.role === 'student'">
                <div class="form-group">
                  <label>学号</label>
                  <input v-model="profileData.student_id" placeholder="请输入学号" class="input" />
                </div>
                <div class="form-group">
                  <label>专业</label>
                  <input v-model="profileData.major" placeholder="请输入专业" class="input" />
                </div>
                <div class="form-group">
                  <label>年级</label>
                  <input v-model="profileData.grade" placeholder="请输入年级" class="input" />
                </div>
              </template>
              
              <template v-if="user?.role === 'teacher'">
                <div class="form-group">
                  <label>工号</label>
                  <input v-model="profileData.employee_id" placeholder="请输入工号" class="input" />
                </div>
                <div class="form-group">
                  <label>学科</label>
                  <input v-model="profileData.subject" placeholder="请输入学科" class="input" />
                </div>
                <div class="form-group">
                  <label>部门</label>
                  <input v-model="profileData.department" placeholder="请输入部门" class="input" />
                </div>
              </template>
            </div>
            
            <div class="form-group full-width mt-4">
              <label>个性签名</label>
              <textarea v-model="profileData.signature" placeholder="请输入个性签名" rows="3" class="input"></textarea>
            </div>
            
            <div class="form-actions mt-6">
              <button type="submit" class="btn btn-primary">保存修改配置</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'

const user = ref<any>(null)
const profileData = reactive({
  name: '', email: '', gender: '', phone: '', signature: '',
  student_id: '', employee_id: '', major: '', grade: '', subject: '', department: ''
})

const getRoleText = (role: string) => ({ admin: '系统管理员', student: '学生', teacher: '老师' }[role] || role)

const fetchProfile = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/auth/profile/', { headers: { Authorization: `Bearer ${token}` } })
    user.value = response.data
    Object.assign(profileData, {
      name: response.data.name || '', email: response.data.email || '', gender: response.data.gender || '',
      phone: response.data.phone || '', signature: response.data.signature || '', student_id: response.data.student_id || '',
      employee_id: response.data.employee_id || '', major: response.data.major || '', grade: response.data.grade || '',
      subject: response.data.subject || '', department: response.data.department || ''
    })
  } catch (error) { console.error('获取用户信息失败', error) }
}

const saveProfile = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.put('http://127.0.0.1:8000/api/auth/profile/', profileData, { headers: { Authorization: `Bearer ${token}` } })
    user.value = response.data
    localStorage.setItem('user', JSON.stringify(response.data))
    alert('管理员配置保存成功')
  } catch (error) { alert('保存失败') }
}

onMounted(() => {
  const storedUser = localStorage.getItem('user')
  if (storedUser) user.value = JSON.parse(storedUser)
  fetchProfile()
})
</script>

<style scoped>
.page-container { max-width: 1200px; margin: 0 auto; padding: var(--spacing-6); animation: fadeIn var(--transition-normal); }
.page-header { margin-bottom: var(--spacing-8); }
.page-header h2 { font-size: var(--font-size-3xl); font-family: var(--font-sf); color: var(--text-primary); margin-bottom: var(--spacing-2); }
.subtitle { color: var(--text-secondary); font-size: var(--font-size-sm); }

.profile-container { display: grid; grid-template-columns: 360px 1fr; gap: var(--spacing-8); }
.card { background: var(--bg-primary); border-radius: var(--border-radius-xl); box-shadow: var(--shadow-sm); border: 1px solid var(--border-light); overflow: hidden; }

/* 左侧概览卡片 */
.profile-card { height: fit-content; }
.profile-header { padding: var(--spacing-8) var(--spacing-6); text-align: center; border-bottom: 1px solid var(--border-light); background: var(--bg-secondary); display: flex; flex-direction: column; align-items: center; }
.avatar-gradient { width: 90px; height: 90px; border-radius: var(--border-radius-full); background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary-dark) 100%); display: flex; justify-content: center; align-items: center; font-size: 36px; color: white; font-weight: 700; margin-bottom: var(--spacing-4); box-shadow: var(--shadow-md); }
.user-info h3 { margin: 0 0 8px; color: var(--text-primary); font-size: var(--font-size-xl); font-weight: 600; }
.role-tag { display: inline-block; padding: 4px 16px; background: var(--primary-soft); color: var(--primary-dark); border-radius: var(--border-radius-full); font-size: var(--font-size-xs); font-weight: 600; margin-bottom: 12px; }
.points-badge { margin: 0; color: var(--text-secondary); font-size: var(--font-size-sm); }
.points-badge strong { color: var(--warning-color); font-size: var(--font-size-lg); }

.profile-details { padding: var(--spacing-6); display: flex; flex-direction: column; gap: 0; }
.detail-item { display: flex; justify-content: space-between; padding: var(--spacing-4) 0; border-bottom: 1px dashed var(--border-color); }
.detail-item:last-child { border-bottom: none; }
.label { color: var(--text-tertiary); font-size: var(--font-size-sm); font-weight: 600; }
.value { color: var(--text-primary); font-weight: 500; }

/* 右侧编辑卡片 */
.card-header { padding: var(--spacing-6) var(--spacing-8); border-bottom: 1px solid var(--border-light); }
.card-header h3 { font-size: var(--font-size-lg); color: var(--text-primary); font-weight: 600; margin: 0; }
.card-body { padding: var(--spacing-8); }
.form-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--spacing-6); }
.form-group { display: flex; flex-direction: column; gap: 8px; }
.form-group label { color: var(--text-secondary); font-size: var(--font-size-sm); font-weight: 500; }
.input { width: 100%; padding: 12px 16px; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: var(--border-radius-lg); font-size: var(--font-size-base); color: var(--text-primary); transition: all var(--transition-fast); }
.input:focus { background: var(--bg-primary); border-color: var(--primary-color); box-shadow: 0 0 0 3px var(--primary-color-10); outline: none; }
.full-width { grid-column: 1 / -1; }
.mt-4 { margin-top: var(--spacing-4); }
.mt-6 { margin-top: var(--spacing-6); }

.form-actions { display: flex; justify-content: flex-end; }
.btn { padding: 12px 28px; border-radius: var(--border-radius-lg); font-weight: 500; font-size: var(--font-size-sm); transition: all var(--transition-fast); cursor: pointer; border: none; }
.btn-primary { background: var(--primary-color); color: white; box-shadow: 0 4px 12px rgba(13, 148, 136, 0.2); }
.btn-primary:hover { background: var(--primary-dark); transform: translateY(-2px); box-shadow: 0 6px 16px rgba(13, 148, 136, 0.3); }

.fade-in { animation: fadeIn var(--transition-normal); }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

@media (max-width: 860px) { .profile-container { grid-template-columns: 1fr; } .profile-card { max-width: 500px; margin: 0 auto; width: 100%; } }
@media (max-width: 640px) { .form-grid { grid-template-columns: 1fr; } }
</style>