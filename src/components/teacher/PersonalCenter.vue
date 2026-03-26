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
        <p class="role-tag">老师</p>
        <p class="points">积分: {{ user?.points || 0 }}</p>
        <div class="action-buttons">
          <button @click="isEditing = !isEditing" class="btn-edit-profile">
            {{ isEditing ? '取消' : '修改资料' }}
          </button>
          <button @click="showPasswordModal = true" class="btn-change-password">
            <IconLock class="btn-icon" />
            <span>修改密码</span>
          </button>
        </div>
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
              <span class="label">工号</span>
              <span class="value">{{ user?.employee_id || '未设置' }}</span>
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
              <span class="label">学科</span>
              <span class="value">{{ user?.subject || '未设置' }}</span>
            </div>
            <div class="info-item">
              <span class="label">部门</span>
              <span class="value">{{ user?.department || '未设置' }}</span>
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
              <label>工号</label>
              <input v-model="formData.employee_id" placeholder="请输入工号" />
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
              <label>学科</label>
              <input v-model="formData.subject" placeholder="请输入学科" />
            </div>
            <div class="form-group">
              <label>部门</label>
              <input v-model="formData.department" placeholder="请输入部门" />
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

    <!-- 修改密码弹窗 -->
    <div v-if="showPasswordModal" class="modal-overlay" @click="closePasswordModal">
      <div class="password-modal" @click.stop>
        <div class="modal-header">
          <div class="modal-title">
            <IconLock class="modal-icon" />
            <h3>修改密码</h3>
          </div>
          <button @click="closePasswordModal" class="close-btn">
            <IconClose class="close-icon" />
          </button>
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
import { IconLock, IconClose } from '../../components/icons'

const user = ref<any>(null)
const isEditing = ref(false)
const showPasswordModal = ref(false)
const passwordLoading = ref(false)
const formData = ref({
  username: '',
  name: '',
  employee_id: '',
  gender: '',
  phone: '',
  email: '',
  subject: '',
  department: '',
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
      employee_id: user.value.employee_id || '',
      gender: user.value.gender || '',
      phone: user.value.phone || '',
      email: user.value.email || '',
      subject: user.value.subject || '',
      department: user.value.department || '',
      signature: user.value.signature || ''
    }
  }
})
</script>

<style scoped>
.page-container { padding: 20px; }
h2 { color: var(--text-primary); font-family: var(--font-sf); margin-bottom: 20px; }
.personal-info { display: flex; gap: 40px; }
.avatar-section { text-align: center; }
.avatar { position: relative; display: inline-block; cursor: pointer; }
.avatar img { width: 150px; height: 150px; border-radius: 50%; object-fit: cover; border: 3px solid var(--primary-color); }
.avatar-edit { position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.6); color: white; padding: 8px; border-radius: 0 0 75px 75px; font-size: 12px; }
.avatar-edit:hover { background: rgba(0,0,0,0.8); }
.avatar-section h3 { margin: 15px 0 5px; color: var(--text-primary); }
.role-tag { display: inline-block; background: rgba(13, 148, 136, 0.1); color: var(--primary-color); padding: 2px 12px; border-radius: 12px; font-size: 12px; margin: 5px 0 10px; }
.points { font-size: 16px; color: var(--secondary-color); margin: 0 0 15px; font-weight: 600; }
.action-buttons { display: flex; gap: 10px; }
.btn-edit-profile { padding: 10px 20px; background: var(--primary-color); color: white; border: none; border-radius: var(--border-radius); cursor: pointer; font-size: 14px; font-weight: 500; transition: all var(--transition-fast); }
.btn-edit-profile:hover { background: var(--primary-dark); }
.btn-change-password { display: inline-flex; align-items: center; gap: 6px; padding: 10px 20px; background: var(--success-color); color: white; border: none; border-radius: var(--border-radius); cursor: pointer; font-size: 14px; font-weight: 500; transition: all var(--transition-fast); }
.btn-change-password:hover { background: #059669; }
.btn-icon { width: 16px; height: 16px; }
.info-section { flex: 1; }
.info-card { background: white; padding: 30px; border-radius: var(--border-radius-lg); box-shadow: var(--shadow-md); border: 1px solid var(--border-light); }
.info-card h3 { margin: 0 0 20px; color: var(--text-primary); border-bottom: 2px solid var(--primary-color); padding-bottom: 10px; font-family: var(--font-sf); }

/* 查看模式样式 */
.info-view { display: flex; flex-direction: column; gap: 15px; }
.info-item { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid var(--border-light); }
.info-item .label { color: var(--text-tertiary); font-weight: 500; }
.info-item .value { color: var(--text-primary); font-weight: 500; }

/* 编辑模式样式 */
.edit-form { display: flex; flex-direction: column; gap: 15px; }
.form-group { display: flex; flex-direction: column; gap: 8px; }
.form-group label { display: block; margin-bottom: 8px; color: var(--text-secondary); font-weight: 500; }
.form-group input, .form-group select, .form-group textarea { width: 100%; padding: 12px 16px; border: 1px solid var(--border-color); border-radius: var(--border-radius); box-sizing: border-box; font-size: 14px; transition: all var(--transition-fast); }
.form-group input:focus, .form-group select:focus, .form-group textarea:focus { outline: none; border-color: var(--primary-color); box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1); }
.form-group input[readonly] { background: var(--bg-tertiary); cursor: not-allowed; }
.form-actions { padding-top: 10px; display: flex; gap: 10px; }
.btn-cancel { padding: 12px 24px; border: 1px solid var(--border-color); background: white; border-radius: var(--border-radius); cursor: pointer; color: var(--text-secondary); font-weight: 500; transition: all var(--transition-fast); }
.btn-cancel:hover { border-color: var(--primary-color); color: var(--primary-color); }
.btn-submit { padding: 12px 24px; background: var(--primary-color); color: white; border: none; border-radius: var(--border-radius); cursor: pointer; font-weight: 500; transition: all var(--transition-fast); }
.btn-submit:hover { background: var(--primary-dark); }
.btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }

@media (max-width: 768px) {
  .personal-info { flex-direction: column; align-items: center; }
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
}

.password-modal {
  background: white;
  border-radius: var(--border-radius-lg);
  width: 90%;
  max-width: 450px;
  box-shadow: var(--shadow-xl);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-light);
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.modal-icon {
  width: 24px;
  height: 24px;
  color: var(--primary-color);
}

.modal-header h3 {
  margin: 0;
  color: var(--text-primary);
  font-size: 18px;
  font-family: var(--font-sf);
}

.close-btn {
  width: 36px;
  height: 36px;
  background: var(--bg-tertiary);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.close-icon {
  width: 18px;
  height: 18px;
  color: var(--text-secondary);
}

.close-btn:hover {
  background: var(--bg-secondary);
}

.password-form {
  padding: 24px;
}

.password-form .form-group {
  margin-bottom: 16px;
}

.password-form .form-group label {
  display: block;
  margin-bottom: 8px;
  color: var(--text-secondary);
  font-weight: 500;
}

.password-form .form-group input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  box-sizing: border-box;
  font-size: 14px;
  transition: all var(--transition-fast);
}

.password-form .form-group input:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
}

.password-form .form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}
</style>
