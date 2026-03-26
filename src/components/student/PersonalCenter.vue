<template>
  <div class="page-container">
    <h2>个人中心</h2>
    
    <!-- 个人统计卡片 -->
    <div class="stats-section">
      <div class="stat-card">
        <div class="stat-icon">🎓</div>
        <div class="stat-content">
          <div class="stat-value">{{ user?.points || 0 }}</div>
          <div class="stat-label">我的积分</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📚</div>
        <div class="stat-content">
          <div class="stat-value">{{ user?.resource_count || 0 }}</div>
          <div class="stat-label">上传资源</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">💬</div>
        <div class="stat-content">
          <div class="stat-value">{{ user?.post_count || 0 }}</div>
          <div class="stat-label">发布帖子</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">⭐</div>
        <div class="stat-content">
          <div class="stat-value">{{ user?.collection_count || 0 }}</div>
          <div class="stat-label">收藏资源</div>
        </div>
      </div>
    </div>
    
    <div class="personal-info">
      <div class="avatar-section">
        <div class="avatar" @click="triggerFileInput">
          <img :src="user?.avatar || defaultAvatar" alt="头像" />
          <input type="file" ref="fileInput" style="display: none" @change="handleAvatarUpload" />
          <div class="avatar-edit">更换头像</div>
        </div>
        <h3>{{ user?.name || '未设置' }}</h3>
        <p class="role-tag">学生</p>
        <p class="student-id">{{ user?.student_id || '未设置' }}</p>
        <div class="action-buttons">
          <button @click="isEditing = !isEditing" class="btn-edit-profile">
            {{ isEditing ? '取消' : '修改资料' }}
          </button>
          <button @click="showPasswordModal = true" class="btn-change-password">
            🔑 修改密码
          </button>
        </div>
      </div>
      
      <div class="info-section">
        <div class="info-card">
          <h3>基本信息</h3>
          
          <!-- 查看模式 -->
          <div v-if="!isEditing" class="info-view">
            <div class="info-grid">
              <div class="info-item">
                <span class="label">用户名</span>
                <span class="value">{{ user?.username || '未设置' }}</span>
              </div>
              <div class="info-item">
                <span class="label">姓名</span>
                <span class="value">{{ user?.name || '未设置' }}</span>
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
                <span class="label">指导老师</span>
                <span class="value">{{ user?.supervisor?.name || '未设置' }}</span>
              </div>
            </div>
            <div class="info-item full-width">
              <span class="label">个性签名</span>
              <span class="value">{{ user?.signature || '未设置' }}</span>
            </div>
          </div>
          
          <!-- 编辑模式 -->
          <form v-else @submit.prevent="saveProfile" class="edit-form">
            <div class="form-grid">
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
            </div>
            <div class="form-group full-width">
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

    <!-- 修改密码弹窗 -->
    <div v-if="showPasswordModal" class="modal-overlay" @click="closePasswordModal">
      <div class="password-modal" @click.stop>
        <div class="modal-header">
          <h3>🔑 修改密码</h3>
          <button @click="closePasswordModal" class="close-btn">✕</button>
        </div>
        <form @submit.prevent="handleChangePassword" class="password-form">
          <div class="form-group">
            <label>当前密码</label>
            <input 
              v-model="passwordForm.old_password" 
              type="password" 
              placeholder="请输入当前密码" 
              required 
            />
          </div>
          <div class="form-group">
            <label>新密码</label>
            <input 
              v-model="passwordForm.new_password" 
              type="password" 
              placeholder="请输入新密码（至少 6 位）" 
              required 
            />
          </div>
          <div class="form-group">
            <label>确认新密码</label>
            <input 
              v-model="passwordForm.confirm_password" 
              type="password" 
              placeholder="请再次输入新密码" 
              required 
            />
          </div>
          <div class="form-actions">
            <button type="button" @click="closePasswordModal" class="btn-cancel">取消</button>
            <button type="submit" class="btn-submit" :disabled="passwordLoading">
              {{ passwordLoading ? '修改中...' : '确认修改' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const user = ref<any>(null)
const isEditing = ref(false)
const showPasswordModal = ref(false)
const passwordLoading = ref(false)
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
const passwordForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
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

const closePasswordModal = () => {
  showPasswordModal.value = false
  passwordForm.value = {
    old_password: '',
    new_password: '',
    confirm_password: ''
  }
}

const handleChangePassword = async () => {
  // 验证新密码
  if (passwordForm.value.new_password.length < 6) {
    alert('新密码长度不能少于 6 位')
    return
  }
  
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    alert('两次输入的新密码不一致')
    return
  }
  
  passwordLoading.value = true
  
  try {
    const token = localStorage.getItem('token')
    await axios.post('http://127.0.0.1:8000/api/auth/change-password/', {
      old_password: passwordForm.value.old_password,
      new_password: passwordForm.value.new_password
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    alert('密码修改成功，请重新登录')
    closePasswordModal()
    
    // 退出登录
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    window.location.href = '/login'
  } catch (error: any) {
    const message = error.response?.data?.error || '密码修改失败'
    alert(message)
  } finally {
    passwordLoading.value = false
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
.page-container {
  padding: 20px;
  background-color: var(--color-background);
  min-height: 100vh;
}

.page-container h2 {
  color: var(--color-text-primary);
  font-size: var(--font-size-h2);
  font-weight: 600;
  margin-bottom: 30px;
  text-align: center;
}

/* 统计卡片样式 */
.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: var(--color-card-bg);
  border-radius: var(--border-radius-lg);
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: var(--box-shadow-sm);
  transition: all 0.3s ease;
  border: 1px solid var(--color-border);
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--box-shadow-md);
}

.stat-icon {
  font-size: 48px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary-light);
  border-radius: var(--border-radius-full);
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: var(--font-size-h3);
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 4px;
}

.stat-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.personal-info {
  display: flex;
  gap: 40px;
  margin-bottom: 40px;
}

.avatar-section {
  text-align: center;
  flex-shrink: 0;
  width: 250px;
}

.avatar {
  position: relative;
  display: inline-block;
  cursor: pointer;
  transition: all 0.3s ease;
}

.avatar:hover {
  transform: scale(1.05);
}

.avatar img {
  width: 160px;
  height: 160px;
  border-radius: var(--border-radius-full);
  object-fit: cover;
  border: 4px solid var(--color-primary);
  box-shadow: var(--box-shadow-md);
}

.avatar-edit {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 10px;
  border-radius: 0 0 80px 80px;
  font-size: 12px;
  transition: all 0.3s ease;
}

.avatar-edit:hover {
  background: rgba(0, 0, 0, 0.8);
}

.avatar-section h3 {
  margin: 20px 0 8px;
  color: var(--color-text-primary);
  font-size: var(--font-size-h4);
  font-weight: 600;
}

.role-tag {
  display: inline-block;
  background: var(--color-primary-light);
  color: var(--color-primary);
  padding: 4px 16px;
  border-radius: 16px;
  font-size: 12px;
  margin: 8px 0 12px;
  font-weight: 500;
}

.student-id {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin: 0 0 20px;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  max-width: 200px;
  margin: 0 auto;
}

.btn-edit-profile {
  padding: 12px 24px;
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  color: black;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
  width: 100%;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.btn-edit-profile:hover {
  background: linear-gradient(135deg, var(--color-primary-dark) 0%, var(--color-primary) 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.4);
  color: black;
}

.btn-change-password {
  padding: 12px 24px;
  background: linear-gradient(135deg, var(--color-success) 0%, var(--color-success-dark) 100%);
  color: black;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
  width: 100%;
  box-shadow: 0 4px 12px rgba(103, 194, 58, 0.3);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.btn-change-password:hover {
  background: linear-gradient(135deg, var(--color-success-dark) 0%, var(--color-success) 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(103, 194, 58, 0.4);
  color: black;
}

.info-section {
  flex: 1;
}

.info-card {
  background: var(--color-card-bg);
  padding: 32px;
  border-radius: var(--border-radius-lg);
  box-shadow: var(--box-shadow-sm);
  border: 1px solid var(--color-border);
}

.info-card h3 {
  margin: 0 0 24px;
  color: var(--color-text-primary);
  border-bottom: 2px solid var(--color-primary);
  padding-bottom: 12px;
  font-size: var(--font-size-h4);
  font-weight: 600;
}

/* 查看模式样式 */
.info-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 16px;
  background: var(--color-background);
  border-radius: var(--border-radius);
  border: 1px solid var(--color-border);
  transition: all 0.3s ease;
}

.info-item:hover {
  box-shadow: var(--box-shadow-sm);
  transform: translateY(-1px);
}

.info-item.full-width {
  grid-column: 1 / -1;
}

.info-item .label {
  color: var(--color-text-secondary);
  font-weight: 500;
  font-size: var(--font-size-sm);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-item .value {
  color: var(--color-text-primary);
  font-weight: 500;
  font-size: var(--font-size-base);
}

/* 编辑模式样式 */
.edit-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  display: block;
  color: var(--color-text-secondary);
  font-weight: 500;
  font-size: var(--font-size-sm);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
  box-sizing: border-box;
  font-size: var(--font-size-base);
  transition: all 0.3s ease;
  background: white;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}

.form-group input[readonly] {
  background: var(--color-background);
  cursor: not-allowed;
  color: var(--color-text-secondary);
}

.form-actions {
  padding-top: 10px;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-cancel {
  padding: 12px 28px;
  border: 1px solid var(--color-border);
  background: white;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  color: var(--color-text-primary);
}

.btn-cancel:hover {
  background: var(--color-background);
  border-color: var(--color-text-secondary);
}

.btn-submit {
  padding: 12px 28px;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-submit:hover {
  background: var(--color-primary-hover);
  transform: translateY(-1px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .personal-info {
    flex-direction: column;
    align-items: center;
  }
  
  .avatar-section {
    width: 100%;
    margin-bottom: 30px;
  }
  
  .stats-section {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .info-card {
    padding: 20px;
  }
}

@media (max-width: 480px) {
  .stats-section {
    grid-template-columns: 1fr;
  }
  
  .page-container {
    padding: 16px;
  }
}

/* 修改密码弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  animation: fadeIn 0.3s ease;
}

.password-modal {
  background: var(--color-card-bg);
  border-radius: var(--border-radius-lg);
  width: 90%;
  max-width: 450px;
  box-shadow: var(--box-shadow-lg);
  border: 1px solid var(--color-border);
  animation: slideIn 0.3s ease;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border);
}

.modal-header h3 {
  margin: 0;
  color: var(--color-text-primary);
  font-size: var(--font-size-h4);
  font-weight: 600;
  border-bottom: none;
  padding-bottom: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: var(--color-text-secondary);
  cursor: pointer;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-full);
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: var(--color-background);
  color: var(--color-text-primary);
  transform: rotate(90deg);
}

.password-form {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: var(--color-text-secondary);
  font-weight: 500;
  font-size: var(--font-size-sm);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
  box-sizing: border-box;
  font-size: var(--font-size-base);
  transition: all 0.3s ease;
  background: white;
}

.form-group input:focus {
  border-color: var(--color-primary);
  outline: none;
  box-shadow: 0 0 0 3px var(--color-primary-light);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.btn-submit:disabled {
  background: var(--color-text-tertiary);
  cursor: not-allowed;
  transform: none;
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
