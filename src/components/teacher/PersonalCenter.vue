<template>
  <div class="page-container">
    <div class="page-header">
      <h2>个人中心</h2>
      <p class="subtitle">管理你的教师档案与系统凭证</p>
    </div>
    
    <div class="personal-info">
      <div class="profile-sidebar card">
        <div class="avatar-wrapper" @click="triggerFileInput">
          <img :src="user?.avatar || defaultAvatar" alt="头像" class="avatar-img" />
          <div class="avatar-overlay">
            <span>更换头像</span>
          </div>
          <input type="file" ref="fileInput" style="display: none" @change="handleAvatarUpload" />
        </div>
        
        <div class="user-titles">
          <h3>{{ user?.name || '未设置' }}</h3>
          <span class="role-badge">教师</span>
        </div>
        
        <div class="action-buttons">
          <button @click="isEditing = !isEditing" :class="['btn', isEditing ? 'btn-secondary' : 'btn-primary']">
            {{ isEditing ? '取消修改' : '修改资料' }}
          </button>
          <button @click="showPasswordModal = true" class="btn btn-outline">
            <IconLock class="btn-icon" />
            修改密码
          </button>
        </div>
      </div>

      <div class="info-main card">
        <div class="card-header">
          <h3>{{ isEditing ? '编辑档案信息' : '基本档案信息' }}</h3>
        </div>

        <div class="card-body">
          <div v-if="!isEditing" class="info-view fade-in">
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
            </div>
            <div class="info-item full-width mt-4">
              <span class="label">个性签名</span>
              <span class="value signature-text">{{ user?.signature || '这家伙很懒，什么都没写~' }}</span>
            </div>
          </div>

          <form v-else @submit.prevent="saveProfile" class="edit-form fade-in">
            <div class="form-grid">
              <div class="form-group">
                <label>用户名</label>
                <input v-model="formData.username" readonly class="input input-readonly" />
              </div>
              <div class="form-group">
                <label>姓名</label>
                <input v-model="formData.name" placeholder="请输入姓名" class="input" />
              </div>
              <div class="form-group">
                <label>工号</label>
                <input v-model="formData.employee_id" placeholder="请输入工号" class="input" />
              </div>
              <div class="form-group">
                <label>性别</label>
                <select v-model="formData.gender" class="input">
                  <option value="">请选择</option>
                  <option value="male">男</option>
                  <option value="female">女</option>
                  <option value="other">其他</option>
                </select>
              </div>
              <div class="form-group">
                <label>手机号</label>
                <input v-model="formData.phone" placeholder="请输入手机号" class="input" />
              </div>
              <div class="form-group">
                <label>邮箱</label>
                <input v-model="formData.email" placeholder="请输入邮箱" type="email" class="input" />
              </div>
              <div class="form-group">
                <label>学科</label>
                <input v-model="formData.subject" placeholder="请输入学科" class="input" />
              </div>
              <div class="form-group">
                <label>部门</label>
                <input v-model="formData.department" placeholder="请输入部门" class="input" />
              </div>
            </div>
            <div class="form-group full-width mt-4">
              <label>个性签名</label>
              <textarea v-model="formData.signature" placeholder="请输入个性签名" rows="3" class="input"></textarea>
            </div>
            <div class="form-actions mt-6">
              <button type="button" @click="isEditing = false" class="btn btn-secondary">取消</button>
              <button type="submit" class="btn btn-primary">保存修改</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="showPasswordModal" class="modal-overlay" @click="closePasswordModal">
      <div class="modal-card slide-up" @click.stop>
        <div class="modal-header">
          <h3><IconLock class="modal-icon" /> 修改密码</h3>
          <button @click="closePasswordModal" class="btn-close">
            <IconClose />
          </button>
        </div>
        <form @submit.prevent="handleChangePassword" class="modal-body">
          <div class="form-group">
            <label>当前密码</label>
            <input v-model="passwordForm.old_password" type="password" placeholder="请输入当前密码" required class="input" />
          </div>
          <div class="form-group">
            <label>新密码</label>
            <input v-model="passwordForm.new_password" type="password" placeholder="请输入新密码（至少 6 位）" required class="input" />
          </div>
          <div class="form-group">
            <label>确认新密码</label>
            <input v-model="passwordForm.confirm_password" type="password" placeholder="请再次输入新密码" required class="input" />
          </div>
          <div class="modal-footer">
            <button type="button" @click="closePasswordModal" class="btn btn-secondary">取消</button>
            <button type="submit" class="btn btn-primary" :disabled="passwordLoading">
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

import { useToast } from '../../composables/useToast'
import axios from 'axios'
import { IconLock, IconClose } from '../../components/icons'

  const toast = useToast()
const user = ref<any>(null)
const isEditing = ref(false)
const showPasswordModal = ref(false)
const passwordLoading = ref(false)
const formData = ref({ username: '', name: '', employee_id: '', gender: '', phone: '', email: '', subject: '', department: '', signature: '' })
const passwordForm = ref({ old_password: '', new_password: '', confirm_password: '' })
const fileInput = ref<HTMLInputElement>()
const defaultAvatar = 'https://via.placeholder.com/150'

const getGenderText = (gender: string) => ({ male: '男', female: '女', other: '其他' }[gender] || '未设置')
const triggerFileInput = () => fileInput.value?.click()

const handleAvatarUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    const file = target.files[0]

    if (file.size > 5 * 1024 * 1024) {
      toast.error('头像文件大小不能超过 5MB')
      return
    }

    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
    if (!allowedTypes.includes(file.type)) {
      toast.error('只支持 JPG、PNG、GIF 格式的图片')
      return
    }

    try {
      const token = localStorage.getItem('token')
      const formData = new FormData()
      formData.append('avatar', file)

      const response = await axios.post('http://127.0.0.1:8000/api/auth/avatar/', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      })

      user.value = response.data.user
      localStorage.setItem('user', JSON.stringify(response.data.user))
      toast.success('头像上传成功')
    } catch (error: any) {
      toast.error(error.response?.data?.error || '头像上传失败')
    }
  }
}

const saveProfile = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.patch('http://127.0.0.1:8000/api/auth/profile/', formData.value, { headers: { Authorization: `Bearer ${token}` } })
    user.value = response.data
    localStorage.setItem('user', JSON.stringify(response.data))
    isEditing.value = false
    toast.success('保存成功')
  } catch (error) {
    toast.error('保存失败')
  }
}

const closePasswordModal = () => {
  showPasswordModal.value = false
  passwordForm.value = { old_password: '', new_password: '', confirm_password: '' }
}

const handleChangePassword = async () => {
  if (passwordForm.value.new_password.length < 6) return toast.info('新密码长度不能少于 6 位')
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) return toast.info('两次输入的新密码不一致')

  passwordLoading.value = true
  try {
    const token = localStorage.getItem('token')
    await axios.post('http://127.0.0.1:8000/api/auth/change-password/', {
      old_password: passwordForm.value.old_password,
      new_password: passwordForm.value.new_password
    }, { headers: { Authorization: `Bearer ${token}` } })

    toast.success('密码修改成功，请重新登录')
    closePasswordModal()
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    window.location.href = '/login'
  } catch (error: any) {
    alert(error.response?.data?.error || '密码修改失败')
  } finally {
    passwordLoading.value = false
  }
}

onMounted(() => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    user.value = JSON.parse(userStr)
    formData.value = { ...user.value }
  }
})
</script>

<style scoped>
/* 此处的 CSS 复用与学生端完全相同的设计语言 */
.page-container { max-width: 1200px; margin: 0 auto; padding: var(--spacing-6); animation: fadeIn var(--transition-normal); }
.page-header { margin-bottom: var(--spacing-8); }
.page-header h2 { font-size: var(--font-size-3xl); font-family: var(--font-sf); color: var(--text-primary); margin-bottom: var(--spacing-2); }
.subtitle { color: var(--text-secondary); font-size: var(--font-size-sm); }
.personal-info { display: grid; grid-template-columns: 320px 1fr; gap: var(--spacing-8); }
.card { background: var(--bg-primary); border-radius: var(--border-radius-xl); box-shadow: var(--shadow-sm); border: 1px solid var(--border-light); overflow: hidden; }

/* 左侧栏 */
.profile-sidebar { padding: var(--spacing-8) var(--spacing-6); text-align: center; display: flex; flex-direction: column; align-items: center; height: fit-content; }
.avatar-wrapper { position: relative; width: 140px; height: 140px; border-radius: var(--border-radius-full); margin-bottom: var(--spacing-6); cursor: pointer; overflow: hidden; box-shadow: var(--shadow-md); border: 4px solid var(--bg-primary); }
.avatar-img { width: 100%; height: 100%; object-fit: cover; transition: transform var(--transition-normal); }
.avatar-overlay { position: absolute; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; color: white; font-size: 14px; opacity: 0; transition: opacity var(--transition-fast); }
.avatar-wrapper:hover .avatar-img { transform: scale(1.05); }
.avatar-wrapper:hover .avatar-overlay { opacity: 1; }
.user-titles h3 { font-size: var(--font-size-xl); color: var(--text-primary); margin-bottom: 8px; font-weight: 600; }
.role-badge { display: inline-block; background: var(--primary-soft); color: var(--primary-dark); padding: 4px 16px; border-radius: var(--border-radius-full); font-size: var(--font-size-xs); font-weight: 600; margin-bottom: 12px; }
.points-tag { color: var(--secondary-color); font-size: var(--font-size-sm); background: #fef3c7; padding: 4px 12px; border-radius: 12px; }
.action-buttons { width: 100%; display: flex; flex-direction: column; gap: var(--spacing-3); margin-top: var(--spacing-8); }
.btn { width: 100%; display: flex; align-items: center; justify-content: center; padding: 12px; border-radius: var(--border-radius-lg); font-weight: 500; font-size: var(--font-size-sm); transition: all var(--transition-fast); cursor: pointer; border: none; }
.btn-primary { background: var(--primary-color); color: white; box-shadow: 0 4px 12px rgba(13, 148, 136, 0.2); }
.btn-primary:hover { background: var(--primary-dark); transform: translateY(-2px); }
.btn-secondary { background: var(--bg-tertiary); color: var(--text-secondary); }
.btn-secondary:hover { background: var(--border-color); }
.btn-outline { background: transparent; border: 1px solid var(--border-color); color: var(--text-secondary); }
.btn-outline:hover { border-color: var(--primary-color); color: var(--primary-color); }
.btn-icon { width: 18px; height: 18px; margin-right: 8px; }

/* 右侧内容 */
.card-header { padding: var(--spacing-6) var(--spacing-8); border-bottom: 1px solid var(--border-light); }
.card-header h3 { font-size: var(--font-size-lg); color: var(--text-primary); font-weight: 600; margin: 0; }
.card-body { padding: var(--spacing-8); }
.info-grid, .form-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--spacing-6); }
.info-item { display: flex; flex-direction: column; gap: 6px; }
.info-item .label { color: var(--text-tertiary); font-size: var(--font-size-xs); text-transform: uppercase; font-weight: 600; }
.info-item .value { color: var(--text-primary); font-size: var(--font-size-base); font-weight: 500; }
.signature-text { background: var(--bg-secondary); padding: var(--spacing-4); border-radius: var(--border-radius-lg); font-style: italic; color: var(--text-secondary); }
.form-group { display: flex; flex-direction: column; gap: 8px; }
.form-group label { color: var(--text-secondary); font-size: var(--font-size-sm); font-weight: 500; }
.input { width: 100%; padding: 12px 16px; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: var(--border-radius-lg); font-size: var(--font-size-base); transition: all var(--transition-fast); }
.input:focus { background: var(--bg-primary); border-color: var(--primary-color); box-shadow: 0 0 0 3px var(--primary-color-10); outline: none; }
.input-readonly { background: var(--bg-tertiary); color: var(--text-tertiary); cursor: not-allowed; }
.full-width { grid-column: 1 / -1; }
.mt-4 { margin-top: var(--spacing-4); }
.mt-6 { margin-top: var(--spacing-6); }
.form-actions { display: flex; justify-content: flex-end; gap: var(--spacing-4); }
.form-actions .btn { width: auto; padding: 10px 24px; }

/* 弹窗 */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 50; animation: fadeIn var(--transition-fast); }
.modal-card { background: var(--bg-primary); width: 100%; max-width: 440px; border-radius: var(--border-radius-2xl); box-shadow: var(--shadow-xl); }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: var(--spacing-5) var(--spacing-6); border-bottom: 1px solid var(--border-light); background: var(--bg-secondary); }
.modal-header h3 { display: flex; align-items: center; gap: 8px; font-size: var(--font-size-lg); font-weight: 600; margin: 0; }
.modal-icon { width: 22px; height: 22px; color: var(--primary-color); }
.btn-close { background: transparent; border: none; color: var(--text-tertiary); cursor: pointer; border-radius: 50%; padding: 4px; transition: all var(--transition-fast); display: flex; }
.btn-close:hover { background: var(--border-color); color: var(--text-primary); }
.modal-body { padding: var(--spacing-6); display: flex; flex-direction: column; gap: var(--spacing-4); }
.modal-footer { margin-top: var(--spacing-4); display: flex; justify-content: flex-end; gap: var(--spacing-3); }
.modal-footer .btn { width: auto; padding: 10px 20px; }
.fade-in { animation: fadeIn var(--transition-normal); }
.slide-up { animation: slideUp var(--transition-normal); }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

@media (max-width: 860px) { .personal-info { grid-template-columns: 1fr; } .profile-sidebar { max-width: 400px; margin: 0 auto; width: 100%; } }
@media (max-width: 640px) { .info-grid, .form-grid { grid-template-columns: 1fr; } }
</style>