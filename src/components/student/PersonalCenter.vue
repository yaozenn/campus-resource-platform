<template>
  <div class="page-container">
    <h2>个人中心</h2>
    <div class="personal-info">
      <div class="avatar-section">
        <div class="avatar" @click="triggerFileInput">
          <img :src="user?.avatar || defaultAvatar" alt="头像" />
          <input type="file" ref="fileInput" style="display: none" @change="handleAvatarUpload" />
          <div class="avatar-edit">更换头像</div>
        </div>
        <h3>{{ user?.name || '未设置' }}</h3>
        <p class="role-tag">学生</p>
        <p class="points">积分: {{ user?.points || 0 }}</p>
        <button @click="isEditing = !isEditing" class="btn-edit-profile">
          {{ isEditing ? '取消' : '修改资料' }}
        </button>
      </div>
      
      <div class="info-section">
        <div class="info-card">
          <h3>基本信息</h3>
          
          <!-- 查看模式 -->
          <div v-if="!isEditing" class="info-view">
            <div class="info-item">
              <span class="label">用户名</span>
              <span class="value">{{ user?.username || '未设置' }}</span>
            </div>
            <div class="info-item">
              <span class="label">姓名</span>
              <span class="value">{{ user?.name || '未设置' }}</span>
            </div>
            <div class="info-item">
              <span class="label">学号</span>
              <span class="value">{{ user?.student_id || '未设置' }}</span>
            </div>
            <div class="info-item">
              <span class="label">性别</span>
              <span class="value">{{ getGenderText(user?.gender) }}</span>
            </div>
            <div class="info-item">
              <span class="label">手机号</span>
              <span class="value">{{ user?.phone || '未设置' }}</span>
            </div>
            <div class="info-item">
              <span class="label">邮箱</span>
              <span class="value">{{ user?.email || '未设置' }}</span>
            </div>
            <div class="info-item">
              <span class="label">专业</span>
              <span class="value">{{ user?.major || '未设置' }}</span>
            </div>
            <div class="info-item">
              <span class="label">年级</span>
              <span class="value">{{ user?.grade || '未设置' }}</span>
            </div>
            <div class="info-item">
              <span class="label">个性签名</span>
              <span class="value">{{ user?.signature || '未设置' }}</span>
            </div>
          </div>
          
          <!-- 编辑模式 -->
          <form v-else @submit.prevent="saveProfile" class="edit-form">
            <div class="form-group">
              <label>用户名</label>
              <input v-model="formData.username" readonly />
            </div>
            <div class="form-group">
              <label>姓名</label>
              <input v-model="formData.name" placeholder="请输入姓名" />
            </div>
            <div class="form-group">
              <label>学号</label>
              <input v-model="formData.student_id" placeholder="请输入学号" />
            </div>
            <div class="form-group">
              <label>性别</label>
              <select v-model="formData.gender">
                <option value="">请选择</option>
                <option value="male">男</option>
                <option value="female">女</option>
                <option value="other">其他</option>
              </select>
            </div>
            <div class="form-group">
              <label>手机号</label>
              <input v-model="formData.phone" placeholder="请输入手机号" />
            </div>
            <div class="form-group">
              <label>邮箱</label>
              <input v-model="formData.email" placeholder="请输入邮箱" type="email" />
            </div>
            <div class="form-group">
              <label>专业</label>
              <input v-model="formData.major" placeholder="请输入专业" />
            </div>
            <div class="form-group">
              <label>年级</label>
              <input v-model="formData.grade" placeholder="请输入年级" />
            </div>
            <div class="form-group">
              <label>个性签名</label>
              <textarea v-model="formData.signature" placeholder="请输入个性签名" rows="3"></textarea>
            </div>
            <div class="form-actions">
              <button type="button" @click="isEditing = false" class="btn-cancel">取消</button>
              <button type="submit" class="btn-submit">保存修改</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const user = ref<any>(null)
const isEditing = ref(false)
const formData = ref({
  username: '',
  name: '',
  student_id: '',
  gender: '',
  phone: '',
  email: '',
  major: '',
  grade: '',
  signature: ''
})
const fileInput = ref<HTMLInputElement>()
const defaultAvatar = 'https://via.placeholder.com/150'

const getGenderText = (gender: string) => {
  const map: any = { male: '男', female: '女', other: '其他' }
  return map[gender] || '未设置'
}

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleAvatarUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    // 这里可以添加头像上传逻辑
    alert('头像上传功能开发中')
  }
}

const saveProfile = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.patch('http://127.0.0.1:8000/api/auth/profile/', formData.value, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    // 更新本地存储的用户信息
    user.value = response.data
    localStorage.setItem('user', JSON.stringify(response.data))
    alert('保存成功')
  } catch (error) {
    alert('保存失败')
  }
}

onMounted(() => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    user.value = JSON.parse(userStr)
    formData.value = {
      username: user.value.username || '',
      name: user.value.name || '',
      student_id: user.value.student_id || '',
      gender: user.value.gender || '',
      phone: user.value.phone || '',
      email: user.value.email || '',
      major: user.value.major || '',
      grade: user.value.grade || '',
      signature: user.value.signature || ''
    }
  }
})
</script>

<style scoped>
.page-container { padding: 20px; }
.personal-info { display: flex; gap: 40px; }
.avatar-section { text-align: center; }
.avatar { position: relative; display: inline-block; cursor: pointer; }
.avatar img { width: 150px; height: 150px; border-radius: 50%; object-fit: cover; border: 3px solid #409eff; }
.avatar-edit { position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.6); color: white; padding: 8px; border-radius: 0 0 75px 75px; font-size: 12px; }
.avatar-edit:hover { background: rgba(0,0,0,0.8); }
.avatar-section h3 { margin: 15px 0 5px; color: #333; }
.role-tag { display: inline-block; background: #e6f7ff; color: #1890ff; padding: 2px 12px; border-radius: 12px; font-size: 12px; margin: 5px 0 10px; }
.points { font-size: 16px; color: #faad14; margin: 0 0 15px; }
.btn-edit-profile { padding: 8px 20px; background: #409eff; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; }
.btn-edit-profile:hover { background: #66b1ff; }
.info-section { flex: 1; }
.info-card { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.info-card h3 { margin: 0 0 20px; color: #333; border-bottom: 2px solid #409eff; padding-bottom: 10px; }

/* 查看模式样式 */
.info-view { display: flex; flex-direction: column; gap: 15px; }
.info-item { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #f0f0f0; }
.info-item .label { color: #999; font-weight: 500; }
.info-item .value { color: #333; font-weight: 500; }

/* 编辑模式样式 */
.edit-form { display: flex; flex-direction: column; gap: 15px; }
.form-group { display: flex; flex-direction: column; gap: 8px; }
.form-group label { display: block; margin-bottom: 8px; color: #666; font-weight: 500; }
.form-group input, .form-group select, .form-group textarea { width: 100%; padding: 10px 12px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
.form-group input[readonly] { background: #f5f5f5; cursor: not-allowed; }
.form-actions { padding-top: 10px; display: flex; gap: 10px; }
.btn-cancel { padding: 10px 24px; border: 1px solid #ddd; background: white; border-radius: 4px; cursor: pointer; }
.btn-submit { padding: 10px 24px; background: #409eff; color: white; border: none; border-radius: 4px; cursor: pointer; }
.btn-submit:hover { background: #66b1ff; }

@media (max-width: 768px) {
  .personal-info { flex-direction: column; align-items: center; }
}
</style>
