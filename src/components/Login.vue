<template>
  <div class="login-page">
    <div class="login-left">
      <div class="left-content">
        <div class="platform-logo">🎓</div>
        <h1>校园课程资源共享平台</h1>
        <p>汇聚优质课程资源，促进知识共享与交流</p>
        <div class="feature-list">
          <div class="feature-item"><span>📚</span>海量课程资源</div>
          <div class="feature-item"><span>💬</span>师生交流论坛</div>
          <div class="feature-item"><span>🤖</span>AI 智能助手</div>
          <div class="feature-item"><span>🎁</span>积分兑换奖励</div>
        </div>
      </div>
    </div>

    <div class="login-right">
      <div class="login-card">
        <h2>欢迎登录</h2>
        <p class="login-subtitle">请选择您的角色并登录</p>

        <div class="role-selector">
          <div
            v-for="r in roles"
            :key="r.value"
            :class="['role-card', role === r.value ? 'active' : '']"
            @click="role = r.value"
          >
            <span class="role-icon">{{ r.icon }}</span>
            <span class="role-label">{{ r.label }}</span>
            <div class="role-check" v-if="role === r.value">✓</div>
          </div>
        </div>

        <form @submit.prevent="handleSubmit" class="login-form">
          <div class="input-group">
            <span class="input-icon">👤</span>
            <input
              v-model="username"
              placeholder="请输入用户名"
              required
              autocomplete="username"
            />
          </div>
          <div class="input-group">
            <span class="input-icon">🔒</span>
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              placeholder="请输入密码"
              required
              autocomplete="current-password"
            />
            <button type="button" class="toggle-pwd" @click="showPassword = !showPassword">
              {{ showPassword ? '🙈' : '👁️' }}
            </button>
          </div>
          <button type="submit" class="btn-login" :disabled="loading">
            <span v-if="loading">登录中...</span>
            <span v-else>登 录</span>
          </button>
        </form>

        <p class="hint-text">测试账号：admin/admin123 · teacher101/teacher123 · student1001/student123</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
type RoleType = 'admin' | 'student' | 'teacher'
const role = ref<RoleType>('student')
const username = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)

const roles: { value: RoleType; label: string; icon: string }[] = [
  { value: 'student', label: '学生', icon: '🎒' },
  { value: 'teacher', label: '老师', icon: '👨‍🏫' },
  { value: 'admin', label: '管理员', icon: '⚙️' },
]

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

    const r = res.data.user.role
    if (r === 'admin') router.push('/admin')
    else if (r === 'teacher') router.push('/teacher')
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
}

/* 左侧装饰区 */
.login-left {
  flex: 1;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}
.left-content { color: white; max-width: 400px; }
.platform-logo { font-size: 64px; margin-bottom: 24px; }
.left-content h1 {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 16px;
  line-height: 1.3;
}
.left-content p { color: rgba(255,255,255,0.65); font-size: 15px; margin: 0 0 36px; }
.feature-list { display: flex; flex-direction: column; gap: 14px; }
.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: rgba(255,255,255,0.8);
}
.feature-item span { font-size: 20px; }

/* 右侧登录区 */
.login-right {
  width: 480px;
  background: #f4f6fb;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}
.login-card {
  background: white;
  border-radius: 20px;
  padding: 40px 36px;
  width: 100%;
  box-shadow: 0 8px 32px rgba(0,0,0,0.08);
}
.login-card h2 { margin: 0 0 6px; font-size: 24px; color: #1a1a2e; }
.login-subtitle { color: #909399; font-size: 14px; margin: 0 0 28px; }

/* 角色选择 */
.role-selector { display: flex; gap: 12px; margin-bottom: 28px; }
.role-card {
  flex: 1;
  padding: 14px 8px;
  border: 2px solid #ebeef5;
  border-radius: 12px;
  cursor: pointer;
  text-align: center;
  transition: all 0.2s;
  position: relative;
  background: #fafafa;
}
.role-card:hover { border-color: #c6e2ff; background: #f0f7ff; }
.role-card.active {
  border-color: #409eff;
  background: #ecf5ff;
}
.role-icon { display: block; font-size: 28px; margin-bottom: 6px; }
.role-label { font-size: 13px; font-weight: 600; color: #303133; }
.role-check {
  position: absolute;
  top: 6px; right: 8px;
  font-size: 12px;
  color: #409eff;
  font-weight: 700;
}

/* 输入框 */
.login-form { display: flex; flex-direction: column; gap: 16px; }
.input-group {
  display: flex;
  align-items: center;
  border: 1px solid #dcdfe6;
  border-radius: 10px;
  padding: 0 14px;
  gap: 10px;
  transition: border-color 0.2s;
  background: white;
}
.input-group:focus-within { border-color: #409eff; box-shadow: 0 0 0 3px rgba(64,158,255,0.1); }
.input-icon { font-size: 16px; flex-shrink: 0; }
.input-group input {
  flex: 1;
  border: none;
  outline: none;
  padding: 13px 0;
  font-size: 14px;
  color: #303133;
  background: transparent;
}
.toggle-pwd {
  background: none; border: none; cursor: pointer; font-size: 16px; padding: 0; flex-shrink: 0;
}

.btn-login {
  padding: 14px;
  background: linear-gradient(135deg, #409eff, #66b1ff);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 4px;
}
.btn-login:hover { opacity: 0.9; transform: translateY(-1px); box-shadow: 0 6px 16px rgba(64,158,255,0.35); }
.btn-login:disabled { opacity: 0.65; cursor: not-allowed; transform: none; }

.hint-text { margin: 20px 0 0; font-size: 11px; color: #c0c4cc; text-align: center; line-height: 1.8; }

/* 响应式 */
@media (max-width: 768px) {
  .login-left { display: none; }
  .login-right { width: 100%; }
}
</style>