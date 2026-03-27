<template>
  <div class="login-page">
    <div class="animated-bg">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
      <div class="particles">
        <span v-for="n in 20" :key="n" :class="['particle', `p-${n}`]"></span>
      </div>
    </div>

    <div class="login-left">
      <div class="glass-panel">
        <div class="brand-section">
          <div class="logo-container">
            <div class="logo-glow"></div>
            <div class="logo-ring ring-1"></div>
            <div class="logo-ring ring-2"></div>
            <IconBook class="logo-icon" />
          </div>
          <h1 class="brand-title">
            <span class="title-line">校园课程资源</span>
            <span class="title-line highlight">共享平台</span>
          </h1>
          <p class="brand-subtitle">Campus Resource Sharing Platform</p>
        </div>

        <div class="features-section">
          <div class="feature-card" v-for="(feature, index) in features" :key="index" :style="{ animationDelay: `${index * 0.1}s` }">
            <div class="feature-icon-wrapper">
              <component :is="feature.icon" class="feature-icon" />
            </div>
            <div class="feature-content">
              <span class="feature-title">{{ feature.title }}</span>
              <span class="feature-desc">{{ feature.desc }}</span>
            </div>
          </div>
        </div>

        <div class="stats-section">
          <div class="stat-item" v-for="(stat, index) in stats" :key="index">
            <div class="stat-number">{{ stat.value }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="login-right">
      <div class="login-card glass-effect">
        <div class="card-header">
          <div class="welcome-badge">
            <IconSparkles class="badge-icon" />
            <span>Welcome Back</span>
          </div>
          <h2 class="card-title">账号登录</h2>
          <p class="card-subtitle">选择您的身份，开启智慧校园之旅</p>
        </div>

        <div class="role-selector-3d">
          <div
            v-for="r in roles"
            :key="r.value"
            :class="['role-card-3d', role === r.value ? 'active' : '']"
            @click="role = r.value"
          >
            <div class="role-card-inner">
              <div class="role-icon-box">
                <component :is="r.icon" class="role-icon-svg" />
                <div class="role-glow"></div>
              </div>
              <span class="role-name">{{ r.label }}</span>
              <div class="role-indicator" v-if="role === r.value">
                <IconCheck class="indicator-icon" />
              </div>
            </div>
          </div>
        </div>

        <form @submit.prevent="handleSubmit" class="login-form">
          <div class="input-wrapper">
            <label class="input-label">用户名</label>
            <div class="input-group floating" :class="{ 'has-error': usernameError }">
              <IconUser class="input-icon-svg" />
              <input
                v-model="username"
                placeholder="请输入用户名"
                required
                autocomplete="username"
                @focus="activeInput = 'username'"
                @blur="activeInput = ''"
                @input="validateUsernameInput"
              />
              <IconAlertCircle v-if="usernameError" class="error-icon-svg" />
              <div class="input-focus-line" :class="{ active: activeInput === 'username' }"></div>
            </div>
            <transition name="fade">
              <div v-if="usernameError" class="error-message-inline">
                <IconAlertCircle class="error-icon-small" />
                {{ usernameError }}
              </div>
            </transition>
          </div>

          <div class="input-wrapper">
            <label class="input-label">密码</label>
            <div class="input-group floating" :class="{ 'has-error': passwordError }">
              <IconLock class="input-icon-svg" />
              <input
                :type="showPassword ? 'text' : 'password'"
                v-model="password"
                placeholder="请输入密码"
                required
                autocomplete="current-password"
                @focus="activeInput = 'password'"
                @blur="activeInput = ''"
              />
              <button type="button" class="toggle-pwd" @click="showPassword = !showPassword">
                <component :is="showPassword ? IconEye : IconEyeOff" class="toggle-icon" />
              </button>
              <IconAlertCircle v-if="passwordError" class="error-icon-svg" />
              <div class="input-focus-line" :class="{ active: activeInput === 'password' }"></div>
            </div>
            <transition name="fade">
              <div v-if="passwordError" class="error-message-inline">
                <IconAlertCircle class="error-icon-small" />
                {{ passwordError }}
              </div>
            </transition>
          </div>

          <div class="form-options">
            <label class="remember-me">
              <input type="checkbox" v-model="rememberMe" />
              <span class="checkmark"></span>
              <span>记住我</span>
            </label>
            <a href="#" class="forgot-link" @click.prevent="showForgotDialog = true">忘记密码?</a>
          </div>

          <button type="submit" class="btn-login-gradient" :disabled="loading">
            <div class="btn-bg"></div>
            <span class="btn-text" v-if="!loading">
              <IconArrowRight class="btn-icon-left" />
              立即登录
            </span>
            <span class="btn-loading" v-else>
              <span class="loading-spinner"></span>
              登录中...
            </span>
          </button>
        </form>

        <div class="divider">
          <span>测试账号</span>
        </div>

        <div class="test-accounts">
          <div class="account-chip" v-for="(acc, idx) in testAccounts" :key="idx" @click="fillAccount(acc)">
            <span class="chip-role" :class="acc.role">{{ acc.roleLabel }}</span>
            <span class="chip-info">{{ acc.username }}</span>
          </div>
        </div>
      </div>

      <div class="decoration-elements">
        <div class="deco-circle c1"></div>
        <div class="deco-circle c2"></div>
        <div class="deco-dots"></div>
      </div>
    </div>

    <!-- 忘记密码弹窗 -->
    <div v-if="showForgotDialog" class="dialog-overlay" @click="showForgotDialog = false">
      <div class="dialog-content" @click.stop>
        <div class="dialog-header">
          <h3>修改密码</h3>
          <button class="btn-close" @click="showForgotDialog = false">
            <IconClose class="close-icon" />
          </button>
        </div>
        <div class="dialog-body">
          <div class="input-wrapper">
            <label class="input-label">用户名</label>
            <div class="input-group" :class="{ 'has-error': forgotForm.usernameError }">
              <IconUser class="input-icon-svg" />
              <input v-model="forgotForm.username" placeholder="请输入用户名" required @input="validateForgotUsername" />
              <IconAlertCircle v-if="forgotForm.usernameError" class="error-icon-svg" />
            </div>
            <transition name="fade">
              <div v-if="forgotForm.usernameError" class="error-message-inline">
                <IconAlertCircle class="error-icon-small" />
                {{ forgotForm.usernameError }}
              </div>
            </transition>
          </div>
          <div class="input-wrapper">
            <label class="input-label">旧密码</label>
            <div class="input-group" :class="{ 'has-error': forgotForm.oldPasswordError }">
              <IconLock class="input-icon-svg" />
              <input type="password" v-model="forgotForm.oldPassword" placeholder="请输入旧密码" required />
              <IconAlertCircle v-if="forgotForm.oldPasswordError" class="error-icon-svg" />
            </div>
            <transition name="fade">
              <div v-if="forgotForm.oldPasswordError" class="error-message-inline">
                <IconAlertCircle class="error-icon-small" />
                {{ forgotForm.oldPasswordError }}
              </div>
            </transition>
          </div>
          <div class="input-wrapper">
            <label class="input-label">新密码</label>
            <div class="input-group" :class="{ 'has-error': forgotForm.newPasswordError }">
              <IconLock class="input-icon-svg" />
              <input type="password" v-model="forgotForm.newPassword" placeholder="请输入新密码（至少 6 位）" required @input="validateForgotNewPassword" />
              <IconAlertCircle v-if="forgotForm.newPasswordError" class="error-icon-svg" />
            </div>
            <transition name="fade">
              <div v-if="forgotForm.newPasswordError" class="error-message-inline">
                <IconAlertCircle class="error-icon-small" />
                {{ forgotForm.newPasswordError }}
              </div>
            </transition>
            <PasswordStrength v-if="forgotForm.newPassword" :password="forgotForm.newPassword" />
          </div>
          <div class="input-wrapper">
            <label class="input-label">确认新密码</label>
            <div class="input-group" :class="{ 'has-error': forgotForm.confirmPasswordError }">
              <IconLock class="input-icon-svg" />
              <input type="password" v-model="forgotForm.confirmPassword" placeholder="请再次输入新密码" required @input="validateForgotConfirmPassword" />
              <IconAlertCircle v-if="forgotForm.confirmPasswordError" class="error-icon-svg" />
            </div>
            <transition name="fade">
              <div v-if="forgotForm.confirmPasswordError" class="error-message-inline">
                <IconAlertCircle class="error-icon-small" />
                {{ forgotForm.confirmPasswordError }}
              </div>
            </transition>
          </div>
          <button @click="handleChangePassword" class="btn-submit" :disabled="changingPassword">
            <span v-if="!changingPassword">确认修改</span>
            <span v-else class="loading-text">修改中...</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import {
  IconBook,
  IconSettings,
  IconStar,
  IconCheck,
  IconUser,
  IconLock,
  IconEye,
  IconEyeOff,
  IconArrowRight,
  IconSparkles,
  IconCollection,
  IconMessageCircle,
  IconZap,
  IconAlertCircle
} from './icons'
import PasswordStrength from './common/PasswordStrength.vue'
import { validateUsername, validatePassword, validatePasswordMatch } from '@/utils/validation'

const router = useRouter()
type RoleType = 'admin' | 'student' | 'teacher'
const role = ref<RoleType>('student')
const username = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const rememberMe = ref(false)
const activeInput = ref('')
const usernameError = ref('')
const passwordError = ref('')

// 忘记密码弹窗
const showForgotDialog = ref(false)
const changingPassword = ref(false)
const forgotForm = ref({
  username: '',
  oldPassword: '',
  newPassword: '',
  confirmPassword: '',
  usernameError: '',
  oldPasswordError: '',
  newPasswordError: '',
  confirmPasswordError: ''
})

// 验证函数
const validateUsernameInput = () => {
  const result = validateUsername(username.value)
  usernameError.value = result.valid ? '' : (result.message || '')
}

const validatePasswordInput = () => {
  const result = validatePassword(password.value)
  passwordError.value = result.valid ? '' : (result.message || '')
}

const validateForgotUsername = () => {
  const result = validateUsername(forgotForm.value.username)
  forgotForm.value.usernameError = result.valid ? '' : (result.message || '')
}

const validateForgotNewPassword = () => {
  const result = validatePassword(forgotForm.value.newPassword)
  forgotForm.value.newPasswordError = result.valid ? '' : (result.message || '')
}

const validateForgotConfirmPassword = () => {
  const result = validatePasswordMatch(forgotForm.value.newPassword, forgotForm.value.confirmPassword)
  forgotForm.value.confirmPasswordError = result.valid ? '' : (result.message || '')
}

// 页面加载时检查是否有保存的登录信息
onMounted(() => {
  const savedUsername = localStorage.getItem('remember_username')
  const savedRole = localStorage.getItem('remember_role') as RoleType
  if (savedUsername) {
    username.value = savedUsername
    rememberMe.value = true
    if (savedRole) {
      role.value = savedRole
    }
  }
})

const features = [
  { icon: IconCollection, title: '海量资源', desc: '10,000+ 优质课程' },
  { icon: IconMessageCircle, title: '互动社区', desc: '师生交流论坛' },
  { icon: IconZap, title: 'AI 助手', desc: '智能学习辅助' },
  { icon: IconStar, title: '积分奖励', desc: '学习兑换好礼' },
]

const stats = [
  { value: '10K+', label: '课程资源' },
  { value: '5K+', label: '活跃用户' },
  { value: '98%', label: '满意度' },
]

const roles = [
  { value: 'student' as RoleType, label: '学生', icon: IconUser },
  { value: 'teacher' as RoleType, label: '老师', icon: IconBook },
  { value: 'admin' as RoleType, label: '管理员', icon: IconSettings },
]

const testAccounts = [
  { role: 'admin', roleLabel: '管理员', username: 'admin', password: 'admin123' },
  { role: 'student', roleLabel: '学生', username: 's1', password: 's123' },
  { role: 'teacher', roleLabel: '老师', username: 't1', password: 't123' },
]

const fillAccount = (acc: any) => {
  username.value = acc.username
  password.value = acc.password
  role.value = acc.role
}

const handleSubmit = async () => {
  loading.value = true
  try {
    const res = await axios.post('http://127.0.0.1:8000/api/auth/login/', {
      username: username.value,
      password: password.value,
      role: role.value
    })
    localStorage.setItem('token', res.data.access)
    localStorage.setItem('user', JSON.stringify(res.data.user))

    // 处理记住我功能
    if (rememberMe.value) {
      localStorage.setItem('remember_username', username.value)
      localStorage.setItem('remember_role', role.value)
    } else {
      localStorage.removeItem('remember_username')
      localStorage.removeItem('remember_role')
  }

  const handleChangePassword = async () => {
    // 表单验证
    if (!forgotForm.value.username || !forgotForm.value.oldPassword || !forgotForm.value.newPassword) {
      alert('请填写所有必填项')
      return
    }
    if (forgotForm.value.newPassword.length < 6) {
      alert('新密码至少需要6位')
      return
    }
    if (forgotForm.value.newPassword !== forgotForm.value.confirmPassword) {
      alert('两次输入的新密码不一致')
      return
    }

    changingPassword.value = true
    try {
      // 先登录获取token
      const loginRes = await axios.post('http://127.0.0.1:8000/api/auth/login/', {
        username: forgotForm.value.username,
        password: forgotForm.value.oldPassword
      })
      
      const token = loginRes.data.access
      
      // 调用修改密码API
      await axios.post('http://127.0.0.1:8000/api/auth/change-password/', {
        old_password: forgotForm.value.oldPassword,
        new_password: forgotForm.value.newPassword
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      
      alert('密码修改成功！请使用新密码登录')
      showForgotDialog.value = false
      // 清空表单
      forgotForm.value = { username: '', oldPassword: '', newPassword: '', confirmPassword: '' }
    } catch (error: any) {
      console.error('修改密码失败:', error)
      const msg = error.response?.data?.error || error.response?.data?.detail || '修改失败，请检查用户名和密码是否正确'
      alert(msg)
    } finally {
      changingPassword.value = false
    }
  }

  const r = res.data.user.role
    if (r === 'admin') router.push('/admin')
    else if (r === 'teacher') router.push('/teacher/courses')
    else router.push('/student')
  } catch (error: any) {
    const data = error.response?.data
    const msg = data?.non_field_errors?.[0] || data?.detail || data?.username?.[0] || data?.password?.[0] || '登录失败，请检查用户名和密码'
    alert(msg)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

/* Animated Background */
.animated-bg {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #0d9488, #14b8a6);
  top: -200px;
  left: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #7c3aed, #a78bfa);
  bottom: -150px;
  right: -100px;
  animation-delay: -7s;
}

.orb-3 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #f59e0b, #fbbf24);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(50px, -50px) scale(1.1); }
  50% { transform: translate(0, -100px) scale(1); }
  75% { transform: translate(-50px, -50px) scale(0.9); }
}

.particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  animation: particle-float 15s ease-in-out infinite;
}

.p-1 { top: 10%; left: 20%; animation-delay: 0s; }
.p-2 { top: 20%; left: 80%; animation-delay: -1s; }
.p-3 { top: 30%; left: 10%; animation-delay: -2s; }
.p-4 { top: 40%; left: 90%; animation-delay: -3s; }
.p-5 { top: 50%; left: 30%; animation-delay: -4s; }
.p-6 { top: 60%; left: 70%; animation-delay: -5s; }
.p-7 { top: 70%; left: 20%; animation-delay: -6s; }
.p-8 { top: 80%; left: 60%; animation-delay: -7s; }
.p-9 { top: 15%; left: 50%; animation-delay: -8s; }
.p-10 { top: 85%; left: 85%; animation-delay: -9s; }
.p-11 { top: 25%; left: 35%; animation-delay: -10s; }
.p-12 { top: 45%; left: 15%; animation-delay: -11s; }
.p-13 { top: 55%; left: 45%; animation-delay: -12s; }
.p-14 { top: 65%; left: 75%; animation-delay: -13s; }
.p-15 { top: 75%; left: 5%; animation-delay: -14s; }
.p-16 { top: 5%; left: 65%; animation-delay: -1.5s; }
.p-17 { top: 35%; left: 55%; animation-delay: -2.5s; }
.p-18 { top: 95%; left: 25%; animation-delay: -3.5s; }
.p-19 { top: 12%; left: 42%; animation-delay: -4.5s; }
.p-20 { top: 88%; left: 48%; animation-delay: -5.5s; }

@keyframes particle-float {
  0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.3; }
  50% { transform: translate(30px, -30px) scale(1.5); opacity: 0.6; }
}

/* Left Side - Brand */
.login-left {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  position: relative;
  z-index: 1;
}

.glass-panel {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 48px;
  max-width: 480px;
  width: 100%;
}

.brand-section {
  text-align: center;
  margin-bottom: 40px;
}

.logo-container {
  position: relative;
  width: 100px;
  height: 100px;
  margin: 0 auto 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-glow {
  position: absolute;
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #0d9488, #14b8a6);
  border-radius: 24px;
  filter: blur(30px);
  opacity: 0.5;
  animation: pulse-glow 3s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.1); }
}

.logo-ring {
  position: absolute;
  border: 2px solid rgba(13, 148, 136, 0.3);
  border-radius: 50%;
  animation: spin-slow 10s linear infinite;
}

.ring-1 {
  width: 120px;
  height: 120px;
  animation-direction: normal;
}

.ring-2 {
  width: 140px;
  height: 140px;
  animation-direction: reverse;
  animation-duration: 15s;
}

@keyframes spin-slow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.logo-icon {
  width: 48px;
  height: 48px;
  color: white;
  position: relative;
  z-index: 1;
}

.brand-title {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin: 0;
}

.title-line {
  font-size: 32px;
  font-weight: 700;
  color: white;
  font-family: var(--font-sf);
  letter-spacing: -0.5px;
}

.title-line.highlight {
  background: linear-gradient(135deg, #0d9488, #14b8a6, #06b6d4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.brand-subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.5);
  margin: 12px 0 0;
  letter-spacing: 2px;
}

.features-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 40px;
}

.feature-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  animation: slide-in 0.5s ease-out forwards;
  opacity: 0;
  transform: translateX(-20px);
  transition: all 0.3s ease;
}

.feature-card:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(8px);
}

@keyframes slide-in {
  to { opacity: 1; transform: translateX(0); }
}

.feature-icon-wrapper {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, rgba(13, 148, 136, 0.3), rgba(20, 184, 166, 0.3));
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.feature-icon {
  width: 24px;
  height: 24px;
  color: #14b8a6;
}

.feature-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.feature-title {
  font-size: 15px;
  font-weight: 600;
  color: white;
}

.feature-desc {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
}

.stats-section {
  display: flex;
  justify-content: space-around;
  padding: 24px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 28px;
  font-weight: 700;
  color: #14b8a6;
  font-family: var(--font-sf);
}

.stat-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 4px;
}

/* Right Side - Login */
.login-right {
  width: 520px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  position: relative;
  z-index: 1;
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 40px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.card-header {
  text-align: center;
  margin-bottom: 32px;
}

.welcome-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: linear-gradient(135deg, rgba(13, 148, 136, 0.1), rgba(20, 184, 166, 0.1));
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  color: #0d9488;
  margin-bottom: 16px;
}

.badge-icon {
  width: 16px;
  height: 16px;
}

.card-title {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 8px;
  font-family: var(--font-sf);
}

.card-subtitle {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

/* Role Selector */
.role-selector-3d {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
}

.role-card-3d {
  flex: 1;
  perspective: 1000px;
  cursor: pointer;
}

.role-card-inner {
  position: relative;
  padding: 20px 12px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 16px;
  text-align: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform-style: preserve-3d;
}

.role-card-3d:hover .role-card-inner {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px -8px rgba(0, 0, 0, 0.15);
}

.role-card-3d.active .role-card-inner {
  border-color: #0d9488;
  background: linear-gradient(135deg, rgba(13, 148, 136, 0.05), rgba(20, 184, 166, 0.05));
  box-shadow: 0 8px 20px -6px rgba(13, 148, 136, 0.3);
}

.role-icon-box {
  position: relative;
  width: 56px;
  height: 56px;
  margin: 0 auto 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.role-icon-svg {
  width: 28px;
  height: 28px;
  color: #0d9488;
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
}

.role-glow {
  position: absolute;
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, rgba(13, 148, 136, 0.2), rgba(20, 184, 166, 0.2));
  border-radius: 14px;
  filter: blur(12px);
  opacity: 0;
  transition: all 0.3s ease;
}

.role-card-3d.active .role-glow {
  opacity: 1;
}

.role-card-3d.active .role-icon-svg {
  transform: scale(1.1);
}

.role-name {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.role-indicator {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 24px;
  height: 24px;
  background: #0d9488;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: pop-in 0.3s ease;
}

@keyframes pop-in {
  0% { transform: scale(0); }
  70% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.indicator-icon {
  width: 14px;
  height: 14px;
  color: white;
}

/* Login Form */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-label {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.input-group {
  position: relative;
  display: flex;
  align-items: center;
  background: #f9fafb;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  padding: 0 16px;
  transition: all 0.3s ease;
}

.input-group:focus-within {
  border-color: #0d9488;
  background: white;
  box-shadow: 0 0 0 4px rgba(13, 148, 136, 0.1);
}

.input-icon-svg {
  width: 20px;
  height: 20px;
  color: #9ca3af;
  flex-shrink: 0;
}

.input-group input {
  flex: 1;
  border: none;
  outline: none;
  padding: 14px 12px;
  font-size: 15px;
  color: #111827;
  background: transparent;
}

.toggle-pwd {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toggle-icon {
  width: 20px;
  height: 20px;
  color: #9ca3af;
  transition: color 0.2s;
}

.input-group:focus-within .toggle-icon {
  color: #0d9488;
}

.input-focus-line {
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #0d9488, #14b8a6);
  transition: all 0.3s ease;
  transform: translateX(-50%);
  border-radius: 0 0 2px 2px;
}

.input-focus-line.active {
  width: calc(100% - 32px);
}

/* Form Options */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #6b7280;
}

.remember-me input {
  display: none;
}

.checkmark {
  width: 18px;
  height: 18px;
  border: 2px solid #d1d5db;
  border-radius: 4px;
  transition: all 0.2s;
  position: relative;
}

.remember-me input:checked + .checkmark {
  background: #0d9488;
  border-color: #0d9488;
}

.remember-me input:checked + .checkmark::after {
  content: '';
  position: absolute;
  left: 5px;
  top: 2px;
  width: 4px;
  height: 8px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.forgot-link {
  font-size: 14px;
  color: #0d9488;
  text-decoration: none;
  transition: color 0.2s;
}

.forgot-link:hover {
  color: #0f766e;
}

/* Login Button */
.btn-login-gradient {
  position: relative;
  padding: 16px;
  border: none;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #0d9488, #14b8a6, #06b6d4);
  background-size: 200% 200%;
  animation: gradient-shift 3s ease infinite;
}

@keyframes gradient-shift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.btn-text, .btn-loading {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: white;
}

.btn-icon-left {
  width: 20px;
  height: 20px;
  transition: transform 0.3s;
}

.btn-login-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px -8px rgba(13, 148, 136, 0.4);
}

.btn-login-gradient:hover .btn-icon-left {
  transform: translateX(4px);
}

.btn-login-gradient:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Divider */
.divider {
  display: flex;
  align-items: center;
  margin: 24px 0;
  gap: 16px;
}

.divider::before, .divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, #e5e7eb, transparent);
}

.divider span {
  font-size: 12px;
  color: #9ca3af;
  white-space: nowrap;
}

/* Test Accounts */
.test-accounts {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.account-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.account-chip:hover {
  background: #0d9488;
  border-color: #0d9488;
}

.account-chip:hover .chip-role,
.account-chip:hover .chip-info {
  color: white;
}

.chip-role {
  font-size: 11px;
  font-weight: 600;
  color: #0d9488;
  padding: 2px 8px;
  background: rgba(13, 148, 136, 0.1);
  border-radius: 10px;
  transition: all 0.2s;
}

.chip-info {
  font-size: 12px;
  color: #374151;
  transition: all 0.2s;
}

/* Decoration */
.decoration-elements {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  overflow: hidden;
}

.deco-circle {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(13, 148, 136, 0.1);
}

.c1 {
  width: 300px;
  height: 300px;
  top: -100px;
  right: -100px;
  animation: float-slow 20s ease-in-out infinite;
}

.c2 {
  width: 200px;
  height: 200px;
  bottom: -50px;
  left: -50px;
  animation: float-slow 15s ease-in-out infinite reverse;
}

@keyframes float-slow {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(30px, -30px); }
}

.deco-dots {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image: radial-gradient(rgba(13, 148, 136, 0.1) 1px, transparent 1px);
  background-size: 30px 30px;
  opacity: 0.5;
}

/* Responsive */
@media (max-width: 1024px) {
  .login-left {
    display: none;
  }
  
  .login-right {
    width: 100%;
    padding: 20px;
  }
}

@media (max-width: 480px) {
  .login-card {
    padding: 28px 20px;
  }
  
  .role-selector-3d {
    flex-direction: column;
  }
  
  .test-accounts {
    flex-direction: column;
  }
  
  .account-chip {
    justify-content: center;
  }
}

/* 忘记密码弹窗样式 */
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
  animation: fade-in 0.3s ease;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

.dialog-content {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 420px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slide-up 0.3s ease;
}

@keyframes slide-up {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.dialog-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.btn-close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  color: #9ca3af;
  transition: color 0.2s;
}

.btn-close:hover {
  color: #374151;
}

.close-icon {
  width: 24px;
  height: 24px;
}

.dialog-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.btn-submit {
  padding: 14px;
  background: linear-gradient(135deg, #0d9488, #14b8a6);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 8px;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(13, 148, 136, 0.3);
}

.btn-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
</style>
