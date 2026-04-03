<template>
  <div class="login-page">
    <!-- 动态背景 -->
    <div class="animated-bg">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
      <div class="particles">
        <span v-for="n in 20" :key="n" :class="['particle', `p-${n}`]"></span>
      </div>
    </div>

    <!-- 左栏：纯视觉 -->
    <div class="login-left">
      <div class="visual-area">
        <div class="brand-logo">
          <div class="logo-rings">
            <div class="logo-ring ring-1"></div>
            <div class="logo-ring ring-2"></div>
            <div class="logo-core">
              <IconBook class="logo-icon" />
            </div>
          </div>
        </div>

        <div class="brand-text">
          <h1 class="brand-title">
            <span>校园课程资源</span>
            <span class="highlight">共享平台</span>
          </h1>
          <p class="brand-subtitle">Campus Resource Sharing Platform</p>
        </div>

        <!-- 几何装饰色块 -->
        <div class="geo geo-teal"></div>
        <div class="geo geo-purple"></div>
        <div class="geo geo-amber"></div>
        <div class="geo geo-teal-sm"></div>
        <div class="geo geo-purple-sm"></div>

        <!-- 中央图形 -->
        <div class="center-graphic">
          <div class="orbit orbit-1">
            <div class="dot dot-teal"></div>
          </div>
          <div class="orbit orbit-2">
            <div class="dot dot-purple"></div>
          </div>
          <div class="orbit orbit-3">
            <div class="dot dot-amber"></div>
          </div>
          <div class="graphic-core">
            <IconMessageCircle class="core-icon" />
          </div>
        </div>
      </div>
    </div>

    <!-- 右栏：登录表单 -->
    <div class="login-right">
      <div class="login-card">
        <div class="card-header">
          <div class="welcome-badge">
            <IconSparkles class="badge-icon" />
            <span>Welcome Back</span>
          </div>
          <h2 class="card-title">账号登录</h2>
          <p class="card-subtitle">选择身份，开启智慧校园之旅</p>
        </div>

        <!-- 角色选择：Segmented Control -->
        <div class="role-segment">
          <div class="segment-track">
            <div
              class="segment-thumb"
              :style="{ transform: `translateX(${roleIndex * 100}%)` }"
            ></div>
            <button
              v-for="(r, i) in roles"
              :key="r.value"
              type="button"
              :class="['segment-btn', role === r.value ? 'active' : '']"
              @click="role = r.value; roleIndex = i"
            >
              <component :is="r.icon" class="seg-icon" />
              <span>{{ r.label }}</span>
            </button>
          </div>
        </div>

        <form @submit.prevent="handleSubmit" class="login-form">
          <div class="input-wrapper">
            <label class="input-label">用户名</label>
            <div class="input-group" :class="{ 'has-error': usernameError }">
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
            </div>
            <transition name="fade">
              <div v-if="usernameError" class="error-msg">
                <IconAlertCircle class="error-icon-small" />
                {{ usernameError }}
              </div>
            </transition>
          </div>

          <div class="input-wrapper">
            <label class="input-label">密码</label>
            <div class="input-group" :class="{ 'has-error': passwordError }">
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
            </div>
            <transition name="fade">
              <div v-if="passwordError" class="error-msg">
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

          <button type="submit" class="btn-login" :disabled="loading">
            <span class="btn-text" v-if="!loading">
              <IconArrowRight class="btn-icon" />
              立即登录
            </span>
            <span class="btn-loading" v-else>
              <span class="loading-spinner"></span>
              登录中...
            </span>
          </button>
        </form>

        <div class="divider"><span>测试账号</span></div>

        <div class="test-accounts">
          <div
            class="account-chip"
            v-for="(acc, idx) in testAccounts"
            :key="idx"
            @click="fillAccount(acc)"
          >
            <span class="chip-role" :class="acc.role">{{ acc.roleLabel }}</span>
            <span class="chip-info">{{ acc.username }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 忘记密码弹窗 -->
    <transition name="fade">
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
                <div v-if="forgotForm.usernameError" class="error-msg">
                  <IconAlertCircle class="error-icon-small" />{{ forgotForm.usernameError }}
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
            </div>
            <div class="input-wrapper">
              <label class="input-label">新密码</label>
              <div class="input-group" :class="{ 'has-error': forgotForm.newPasswordError }">
                <IconLock class="input-icon-svg" />
                <input type="password" v-model="forgotForm.newPassword" placeholder="至少 6 位" required @input="validateForgotNewPassword" />
                <IconAlertCircle v-if="forgotForm.newPasswordError" class="error-icon-svg" />
              </div>
              <transition name="fade">
                <div v-if="forgotForm.newPasswordError" class="error-msg">
                  <IconAlertCircle class="error-icon-small" />{{ forgotForm.newPasswordError }}
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
                <div v-if="forgotForm.confirmPasswordError" class="error-msg">
                  <IconAlertCircle class="error-icon-small" />{{ forgotForm.confirmPasswordError }}
                </div>
              </transition>
            </div>
            <button @click="handleChangePassword" class="btn-submit" :disabled="changingPassword">
              <span v-if="!changingPassword">确认修改</span>
              <span v-else>修改中...</span>
            </button>
          </div>
        </div>
      </div>
    </transition>
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
const roleIndex = ref(0)
const username = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const rememberMe = ref(false)
const activeInput = ref('')
const usernameError = ref('')
const passwordError = ref('')

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

onMounted(() => {
  const savedUsername = localStorage.getItem('remember_username')
  const savedRole = localStorage.getItem('remember_role') as RoleType
  if (savedUsername) {
    username.value = savedUsername
    rememberMe.value = true
    if (savedRole) {
      role.value = savedRole
      roleIndex.value = roles.findIndex(r => r.value === savedRole)
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
  roleIndex.value = roles.findIndex(r => r.value === acc.role)
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

    if (rememberMe.value) {
      localStorage.setItem('remember_username', username.value)
      localStorage.setItem('remember_role', role.value)
    } else {
      localStorage.removeItem('remember_username')
      localStorage.removeItem('remember_role')
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

const handleChangePassword = async () => {
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
    const loginRes = await axios.post('http://127.0.0.1:8000/api/auth/login/', {
      username: forgotForm.value.username,
      password: forgotForm.value.oldPassword
    })
    const token = loginRes.data.access
    await axios.post('http://127.0.0.1:8000/api/auth/change-password/', {
      old_password: forgotForm.value.oldPassword,
      new_password: forgotForm.value.newPassword
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    alert('密码修改成功！请使用新密码登录')
    showForgotDialog.value = false
    forgotForm.value = { username: '', oldPassword: '', newPassword: '', confirmPassword: '', usernameError: '', oldPasswordError: '', newPasswordError: '', confirmPasswordError: '' }
  } catch (error: any) {
    const msg = error.response?.data?.error || error.response?.data?.detail || '修改失败，请检查用户名和密码是否正确'
    alert(msg)
  } finally {
    changingPassword.value = false
  }
}
</script>

<style scoped>
/* ====== Base ====== */
.login-page {
  display: flex;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

/* ====== Animated Background ====== */
.animated-bg {
  position: fixed;
  inset: 0;
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
  width: 600px; height: 600px;
  background: linear-gradient(135deg, #0d9488, #14b8a6);
  top: -200px; left: -100px;
}
.orb-2 {
  width: 500px; height: 500px;
  background: linear-gradient(135deg, #7c3aed, #a78bfa);
  bottom: -150px; right: -100px;
  animation-delay: -7s;
}
.orb-3 {
  width: 400px; height: 400px;
  background: linear-gradient(135deg, #f59e0b, #fbbf24);
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(50px, -50px) scale(1.1); }
  50% { transform: translate(0, -100px) scale(1); }
  75% { transform: translate(-50px, -50px) scale(0.9); }
}

.particles { position: absolute; inset: 0; }
.particle {
  position: absolute;
  width: 3px; height: 3px;
  background: rgba(255, 255, 255, 0.25);
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
  0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.25; }
  50% { transform: translate(30px, -30px) scale(1.5); opacity: 0.5; }
}

/* ====== Left Side: Pure Visual ====== */
.login-left {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
  overflow: hidden;
}

.visual-area {
  position: relative;
  width: 420px;
  height: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* Brand Logo */
.brand-logo {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
}

.logo-rings {
  position: relative;
  width: 88px;
  height: 88px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-ring {
  position: absolute;
  border-radius: 50%;
  border: 1.5px solid rgba(13, 148, 136, 0.35);
}

.ring-1 {
  width: 110px; height: 110px;
  animation: spin-slow 12s linear infinite;
  border-top-color: #0d9488;
}
.ring-2 {
  width: 132px; height: 132px;
  animation: spin-slow 18s linear infinite reverse;
  border-top-color: #7c3aed;
  border-color: rgba(124, 58, 237, 0.25);
  border-top-color: rgba(124, 58, 237, 0.6);
}

@keyframes spin-slow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.logo-core {
  width: 72px; height: 72px;
  background: linear-gradient(135deg, #0d9488, #14b8a6);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 40px rgba(13, 148, 136, 0.4);
  z-index: 1;
}

.logo-icon {
  width: 34px; height: 34px;
  color: white;
}

/* Brand Text */
.brand-text {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  white-space: nowrap;
}

.brand-title {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin: 0 0 10px;
}

.brand-title span {
  font-size: 30px;
  font-weight: 700;
  color: white;
  letter-spacing: -0.5px;
  line-height: 1.2;
}

.brand-title .highlight {
  background: linear-gradient(135deg, #0d9488, #14b8a6, #06b6d4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.brand-subtitle {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
  letter-spacing: 2px;
  margin: 0;
}

/* Geometric Decoration Blocks */
.geo {
  position: absolute;
  border-radius: 28px;
  animation: geo-drift 10s ease-in-out infinite;
  pointer-events: none;
}

/* 大色块 */
.geo-teal {
  width: 160px; height: 160px;
  background: rgba(13, 148, 136, 0.13);
  border: 1px solid rgba(13, 148, 136, 0.2);
  top: 30px; left: -30px;
  border-radius: 40px;
  transform: rotate(-18deg);
  animation-delay: 0s;
}
.geo-purple {
  width: 130px; height: 130px;
  background: rgba(124, 58, 237, 0.11);
  border: 1px solid rgba(124, 58, 237, 0.18);
  bottom: 60px; right: -20px;
  border-radius: 36px;
  transform: rotate(22deg);
  animation-delay: -3.5s;
}
.geo-amber {
  width: 100px; height: 100px;
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.16);
  bottom: 100px; left: 10px;
  border-radius: 28px;
  transform: rotate(-8deg);
  animation-delay: -6s;
}

/* 小色块 */
.geo-teal-sm {
  width: 56px; height: 56px;
  background: rgba(13, 148, 136, 0.18);
  border: 1px solid rgba(13, 148, 136, 0.28);
  top: 80px; right: 30px;
  border-radius: 16px;
  transform: rotate(30deg);
  animation-delay: -2s;
}
.geo-purple-sm {
  width: 44px; height: 44px;
  background: rgba(124, 58, 237, 0.16);
  border: 1px solid rgba(124, 58, 237, 0.24);
  top: 200px; left: 20px;
  border-radius: 14px;
  transform: rotate(-25deg);
  animation-delay: -5s;
}

@keyframes geo-drift {
  0%, 100% { transform: rotate(var(--r, 0deg)) translate(0, 0); }
  33%       { transform: rotate(var(--r, 0deg)) translate(6px, -8px); }
  66%       { transform: rotate(var(--r, 0deg)) translate(-4px, 5px); }
}

.geo-teal   { --r: -18deg; }
.geo-purple { --r:  22deg; }
.geo-amber  { --r:  -8deg; }
.geo-teal-sm   { --r:  30deg; }
.geo-purple-sm { --r: -25deg; }

/* Center Graphic */
.center-graphic {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 200px;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.orbit {
  position: absolute;
  border-radius: 50%;
  border: 1px dashed rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

.orbit-1 {
  width: 140px; height: 140px;
  animation: orbit-spin 8s linear infinite;
}
.orbit-2 {
  width: 180px; height: 180px;
  animation: orbit-spin 12s linear infinite reverse;
}
.orbit-3 {
  width: 220px; height: 220px;
  animation: orbit-spin 16s linear infinite;
}

@keyframes orbit-spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  margin-top: -4px;
}
.dot-teal { background: #14b8a6; box-shadow: 0 0 8px #14b8a6; }
.dot-purple { background: #a78bfa; box-shadow: 0 0 8px #a78bfa; }
.dot-amber { background: #fbbf24; box-shadow: 0 0 8px #fbbf24; }

.graphic-core {
  width: 64px; height: 64px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
  backdrop-filter: blur(10px);
}

.core-icon {
  width: 28px; height: 28px;
  color: rgba(255, 255, 255, 0.6);
}

/* ====== Right Side: Login Card ====== */
.login-right {
  width: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  position: relative;
  z-index: 1;
}

.login-card {
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 40px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 32px 64px -12px rgba(0, 0, 0, 0.3);
}

/* Card Header */
.card-header {
  text-align: center;
  margin-bottom: 28px;
}

.welcome-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: rgba(13, 148, 136, 0.08);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: #0d9488;
  margin-bottom: 14px;
}

.badge-icon {
  width: 14px; height: 14px;
}

.card-title {
  font-size: 26px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 6px;
}

.card-subtitle {
  font-size: 13px;
  color: #9ca3af;
  margin: 0;
}

/* Role Segment Control */
.role-segment {
  margin-bottom: 28px;
}

.segment-track {
  position: relative;
  display: flex;
  background: #f3f4f6;
  border-radius: 12px;
  padding: 4px;
  gap: 0;
}

.segment-thumb {
  position: absolute;
  top: 4px;
  left: 4px;
  width: calc(33.333% - 2.67px);
  height: calc(100% - 8px);
  background: white;
  border-radius: 9px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.12), 0 0 0 1px rgba(0, 0, 0, 0.04);
  transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.segment-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 8px;
  border: none;
  background: transparent;
  border-radius: 9px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  color: #9ca3af;
  transition: color 0.2s;
  position: relative;
  z-index: 1;
}

.segment-btn.active {
  color: #0d9488;
  font-weight: 600;
}

.seg-icon {
  width: 15px; height: 15px;
}

/* Form */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.input-label {
  font-size: 13px;
  font-weight: 500;
  color: #374151;
}

.input-group {
  position: relative;
  display: flex;
  align-items: center;
  background: #f9fafb;
  border: 1.5px solid #e5e7eb;
  border-radius: 11px;
  padding: 0 14px;
  transition: all 0.2s ease;
}

.input-group:focus-within {
  border-color: #0d9488;
  background: white;
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
}

.input-group.has-error {
  border-color: #ef4444;
}

.input-group.has-error:focus-within {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.input-icon-svg {
  width: 18px; height: 18px;
  color: #9ca3af;
  flex-shrink: 0;
}

.input-group input {
  flex: 1;
  border: none;
  outline: none;
  padding: 13px 10px;
  font-size: 14px;
  color: #111827;
  background: transparent;
}

.input-group input::placeholder {
  color: #9ca3af;
}

.error-icon-svg {
  width: 18px; height: 18px;
  color: #ef4444;
  flex-shrink: 0;
}

.toggle-pwd {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
}

.toggle-icon {
  width: 18px; height: 18px;
  color: #9ca3af;
  transition: color 0.2s;
}

.input-group:focus-within .toggle-icon {
  color: #0d9488;
}

.error-msg {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: #ef4444;
}

.error-icon-small {
  width: 13px; height: 13px;
  flex-shrink: 0;
}

/* Form Options */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: -4px;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 7px;
  cursor: pointer;
  font-size: 13px;
  color: #6b7280;
}

.remember-me input { display: none; }

.checkmark {
  width: 17px; height: 17px;
  border: 1.5px solid #d1d5db;
  border-radius: 4px;
  transition: all 0.2s;
  position: relative;
  flex-shrink: 0;
}

.remember-me input:checked + .checkmark {
  background: #0d9488;
  border-color: #0d9488;
}

.remember-me input:checked + .checkmark::after {
  content: '';
  position: absolute;
  left: 4px; top: 1px;
  width: 4px; height: 8px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.forgot-link {
  font-size: 13px;
  color: #0d9488;
  text-decoration: none;
  transition: color 0.2s;
}

.forgot-link:hover { color: #0f766e; }

/* Login Button */
.btn-login {
  padding: 15px;
  background: linear-gradient(135deg, #065f46, #0d9488);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 4px 14px rgba(13, 148, 136, 0.3);
  margin-top: 4px;
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(13, 148, 136, 0.4);
}

.btn-login:active:not(:disabled) {
  transform: translateY(0);
}

.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-text, .btn-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 600;
  color: white;
}

.btn-icon {
  width: 18px; height: 18px;
  transition: transform 0.2s;
}

.btn-login:hover:not(:disabled) .btn-icon {
  transform: translateX(3px);
}

.loading-spinner {
  width: 17px; height: 17px;
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
  margin: 24px 0 16px;
  gap: 12px;
}

.divider::before, .divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #f3f4f6;
}

.divider span {
  font-size: 11px;
  color: #c4c9d4;
  white-space: nowrap;
  letter-spacing: 0.5px;
}

/* Test Accounts */
.test-accounts {
  display: flex;
  gap: 8px;
  justify-content: center;
  flex-wrap: wrap;
}

.account-chip {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 7px 13px;
  background: #f9fafb;
  border: 1px solid #f0f0f0;
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
  transition: color 0.2s;
}

.chip-info {
  font-size: 12px;
  color: #6b7280;
  transition: color 0.2s;
}

/* Dialog */
.dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog-content {
  background: white;
  border-radius: 20px;
  width: 90%;
  max-width: 400px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.2);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #f3f4f6;
}

.dialog-header h3 {
  margin: 0;
  font-size: 17px;
  font-weight: 600;
  color: #111827;
}

.btn-close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  color: #9ca3af;
  display: flex;
  align-items: center;
  transition: color 0.2s;
}

.btn-close:hover { color: #374151; }

.close-icon { width: 22px; height: 22px; }

.dialog-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.btn-submit {
  padding: 13px;
  background: linear-gradient(135deg, #065f46, #0d9488);
  color: white;
  border: none;
  border-radius: 11px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  margin-top: 4px;
  box-shadow: 0 4px 14px rgba(13, 148, 136, 0.25);
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(13, 148, 136, 0.35);
}

.btn-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* Responsive */
@media (max-width: 1024px) {
  .login-left { display: none; }
  .login-right { width: 100%; padding: 20px; }
}

@media (max-width: 480px) {
  .login-card { padding: 28px 20px; }
  .segment-btn span { display: none; }
  .segment-btn { padding: 10px; }
  .test-accounts { flex-direction: column; }
  .account-chip { justify-content: center; }
}
</style>