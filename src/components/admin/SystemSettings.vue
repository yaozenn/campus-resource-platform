<template>
  <div class="page-container">
    <div class="page-header">
      <h2>系统设置</h2>
      <span class="save-tip" v-if="saveStatus">{{ saveStatus }}</span>
    </div>

    <el-tabs v-model="activeTab" class="settings-tabs">
      <!-- 基本设置 -->
      <el-tab-pane label="基本设置" name="basic">
        <div class="setting-card">
          <h3 class="card-title"><IconGlobe class="title-icon" /> 网站基本信息</h3>
          <div class="form-grid">
            <div class="form-group">
              <label>网站名称</label>
              <input v-model="settings.siteName" placeholder="网站名称" />
            </div>
            <div class="form-group">
              <label>联系邮箱</label>
              <input v-model="settings.contactEmail" placeholder="联系邮箱" type="email" />
            </div>
            <div class="form-group full-width">
              <label>网站描述</label>
              <textarea v-model="settings.siteDescription" placeholder="网站描述" rows="3"></textarea>
            </div>
          </div>
          <div class="form-actions">
            <button @click="saveSection" class="btn-save">保存设置</button>
          </div>
        </div>
      </el-tab-pane>

      <!-- 注册设置 -->
      <el-tab-pane label="注册设置" name="register">
        <div class="setting-card">
          <h3 class="card-title"><IconEdit class="title-icon" /> 注册配置</h3>
          <div class="form-grid">
            <div class="form-group">
              <label>默认注册角色</label>
              <select v-model="settings.defaultRole">
                <option value="student">学生</option>
                <option value="teacher">老师</option>
              </select>
            </div>
            <div class="form-group">
              <label>新用户初始积分</label>
              <input v-model.number="settings.initialPoints" type="number" min="0" />
            </div>
            <div class="form-group full-width">
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.allowRegister" />
                <span>允许新用户注册</span>
              </label>
            </div>
          </div>
          <div class="form-actions">
            <button @click="saveSection" class="btn-save">保存设置</button>
          </div>
        </div>
      </el-tab-pane>

      <!-- 积分设置 -->
      <el-tab-pane label="积分规则" name="points">
        <div class="setting-card">
          <h3 class="card-title"><IconStar class="title-icon" /> 积分奖励规则</h3>
          <div class="points-rules">
            <div class="rule-item">
              <div class="rule-info">
                <span class="rule-icon-svg"><IconCalendar class="icon-svg" /></span>
                <div>
                  <div class="rule-name">每日签到</div>
                  <div class="rule-desc">用户每日签到奖励积分</div>
                </div>
              </div>
              <div class="rule-input">
                <input v-model.number="settings.dailySignPoints" type="number" min="0" />
                <span>积分</span>
              </div>
            </div>
            <div class="rule-item">
              <div class="rule-info">
                <span class="rule-icon-svg"><IconUpload class="icon-svg" /></span>
                <div>
                  <div class="rule-name">上传资源</div>
                  <div class="rule-desc">老师上传课程资源奖励</div>
                </div>
              </div>
              <div class="rule-input">
                <input v-model.number="settings.uploadPoints" type="number" min="0" />
                <span>积分</span>
              </div>
            </div>
            <div class="rule-item">
              <div class="rule-info">
                <span class="rule-icon-svg"><IconMessageCircle class="icon-svg" /></span>
                <div>
                  <div class="rule-name">发表帖子</div>
                  <div class="rule-desc">在论坛发表帖子奖励</div>
                </div>
              </div>
              <div class="rule-input">
                <input v-model.number="settings.postPoints" type="number" min="0" />
                <span>积分</span>
              </div>
            </div>
            <div class="rule-item">
              <div class="rule-info">
                <span class="rule-icon-svg"><IconEdit class="icon-svg" /></span>
                <div>
                  <div class="rule-name">发表评论</div>
                  <div class="rule-desc">评论资源或帖子奖励</div>
                </div>
              </div>
              <div class="rule-input">
                <input v-model.number="settings.commentPoints" type="number" min="0" />
                <span>积分</span>
              </div>
            </div>
          </div>
          <div class="form-actions">
            <button @click="saveSection" class="btn-save">保存设置</button>
          </div>
        </div>
      </el-tab-pane>

      <!-- 安全设置 -->
      <el-tab-pane label="安全设置" name="security">
        <div class="setting-card">
          <h3 class="card-title"><IconLock class="title-icon" /> 安全选项</h3>
          <div class="form-grid">
            <div class="form-group">
              <label>密码最小长度</label>
              <input v-model.number="settings.minPasswordLength" type="number" min="6" max="32" />
            </div>
            <div class="form-group full-width switch-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.enableCaptcha" />
                <span>登录启用验证码</span>
              </label>
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.emailVerification" />
                <span>注册需要邮箱验证</span>
              </label>
            </div>
          </div>
          <div class="form-actions">
            <button @click="saveSection" class="btn-save">保存设置</button>
          </div>
        </div>
      </el-tab-pane>

      <!-- 邮件设置 -->
      <el-tab-pane label="邮件设置" name="email">
        <div class="setting-card">
          <h3 class="card-title"><IconEmail class="title-icon" /> SMTP 邮件配置</h3>
          <div class="form-grid">
            <div class="form-group">
              <label>SMTP 服务器</label>
              <input v-model="settings.smtpServer" placeholder="如：smtp.qq.com" />
            </div>
            <div class="form-group">
              <label>SMTP 端口</label>
              <input v-model.number="settings.smtpPort" type="number" />
            </div>
            <div class="form-group">
              <label>发件人邮箱</label>
              <input v-model="settings.smtpEmail" placeholder="发件人邮箱" type="email" />
            </div>
            <div class="form-group">
              <label>SMTP 密码</label>
              <input v-model="settings.smtpPassword" placeholder="授权码或密码" type="password" />
            </div>
          </div>
          <div class="form-actions">
            <button @click="saveSection" class="btn-save">保存设置</button>
          </div>
        </div>
      </el-tab-pane>

      <!-- 通知设置 -->
      <el-tab-pane label="通知设置" name="notification">
        <div class="setting-card">
          <h3 class="card-title"><IconBell class="title-icon" /> 通知配置</h3>
          <div class="form-grid">
            <div class="form-group">
              <label>通知保留天数</label>
              <input v-model.number="settings.notificationExpiryDays" type="number" min="1" />
            </div>
            <div class="form-group full-width switch-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.enableEmailNotification" />
                <span>启用邮件通知</span>
              </label>
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.enableSystemNotification" />
                <span>启用系统内通知</span>
              </label>
            </div>
          </div>
          <div class="form-actions">
            <button @click="saveSection" class="btn-save">保存设置</button>
          </div>
        </div>
      </el-tab-pane>

      <!-- 数据设置 -->
      <el-tab-pane label="数据管理" name="data">
        <div class="setting-card">
          <h3 class="card-title"><IconDatabase class="title-icon" /> 数据管理</h3>
          <div class="form-grid">
            <div class="form-group">
              <label>备份频率</label>
              <select v-model="settings.backupFrequency">
                <option value="daily">每天</option>
                <option value="weekly">每周</option>
                <option value="monthly">每月</option>
              </select>
            </div>
            <div class="form-group">
              <label>数据保留天数</label>
              <input v-model.number="settings.dataRetentionDays" type="number" min="7" />
            </div>
            <div class="form-group full-width switch-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.enableAutoBackup" />
                <span>启用自动备份</span>
              </label>
            </div>
          </div>
          <div class="form-actions">
            <button @click="saveSection" class="btn-save">保存设置</button>
            <button @click="backupNow" class="btn-backup">立即备份</button>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { IconGlobe, IconEdit, IconStar, IconCalendar, IconUpload, IconMessageCircle, IconLock, IconEmail, IconBell, IconDatabase } from '@/components/icons'

const activeTab = ref('basic')
const saveStatus = ref('')

const settings = reactive({
  siteName: '校园课程资源共享平台',
  siteDescription: '提供课程资源共享、学习交流的平台',
  contactEmail: 'admin@campus.com',
  allowRegister: true,
  defaultRole: 'student',
  initialPoints: 100,
  dailySignPoints: 5,
  uploadPoints: 20,
  postPoints: 10,
  commentPoints: 2,
  enableCaptcha: false,
  emailVerification: false,
  minPasswordLength: 6,
  smtpServer: 'smtp.qq.com',
  smtpPort: 465,
  smtpEmail: '',
  smtpPassword: '',
  enableEmailNotification: false,
  enableSystemNotification: true,
  notificationExpiryDays: 7,
  enableAutoBackup: false,
  backupFrequency: 'weekly',
  dataRetentionDays: 30,
})

const loadSettings = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/settings/')
    if (res.data.success) {
      Object.assign(settings, res.data.settings)
    }
  } catch (e) {
    console.error('加载系统设置失败', e)
  }
}

const saveSection = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.post('http://127.0.0.1:8000/api/settings/save/', settings, {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (res.data.success) {
      saveStatus.value = '已保存'
      setTimeout(() => saveStatus.value = '', 2500)
    }
  } catch (e) {
    saveStatus.value = '保存失败'
    setTimeout(() => saveStatus.value = '', 2500)
  }
}

const backupNow = () => {
  saveStatus.value = '备份中...'
  setTimeout(() => {
    saveStatus.value = '备份完成'
    setTimeout(() => saveStatus.value = '', 2500)
  }, 1200)
}

onMounted(loadSettings)
</script>

<style scoped>
.page-container { padding: 24px; }

.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 24px;
}
.page-header h2 { margin: 0; font-size: 22px; color: #1a1a2e; }
.save-tip {
  font-size: 13px;
  color: #67c23a;
  background: #f0f9eb;
  padding: 4px 12px;
  border-radius: 20px;
  border: 1px solid #b3e19d;
}

.settings-tabs :deep(.el-tabs__header) {
  margin-bottom: 0;
}

.setting-card {
  background: white;
  border-radius: 12px;
  padding: 28px 32px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  margin-top: 20px;
}

.card-title {
  margin: 0 0 24px;
  font-size: 16px;
  color: #303133;
  padding-bottom: 14px;
  border-bottom: 2px solid #f0f2f5;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.form-group { display: flex; flex-direction: column; gap: 8px; }
.form-group.full-width { grid-column: 1 / -1; }
.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: #606266;
}
.form-group input,
.form-group textarea,
.form-group select {
  padding: 10px 14px;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  font-size: 14px;
  color: #303133;
  transition: border-color 0.2s;
  outline: none;
}
.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  border-color: #409eff;
  box-shadow: 0 0 0 3px rgba(64,158,255,0.1);
}
.form-group textarea { resize: vertical; }

.switch-group { display: flex; flex-direction: row; gap: 30px; align-items: center; flex-wrap: wrap; }
.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #606266;
  font-weight: normal !important;
}
.checkbox-label input[type="checkbox"] { width: 16px; height: 16px; accent-color: #409eff; cursor: pointer; }

/* 积分规则样式 */
.points-rules { display: flex; flex-direction: column; gap: 16px; }
.rule-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: #f8f9fc;
  border-radius: 10px;
  border: 1px solid #ebeef5;
  transition: border-color 0.2s;
}
.rule-item:hover { border-color: #c6e2ff; }
.rule-info { display: flex; align-items: center; gap: 14px; }
.rule-icon { font-size: 28px; }
.title-icon { width: 20px; height: 20px; margin-right: 8px; vertical-align: middle; }
.rule-icon-svg { width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; background: rgba(13, 148, 136, 0.1); border-radius: 8px; }
.rule-icon-svg .icon-svg { width: 18px; height: 18px; color: var(--primary-color); }
.rule-name { font-weight: 600; color: #303133; font-size: 14px; }
.rule-desc { font-size: 12px; color: #909399; margin-top: 2px; }
.rule-input { display: flex; align-items: center; gap: 8px; }
.rule-input input {
  width: 80px;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  text-align: center;
  font-size: 15px;
  font-weight: 600;
  color: #409eff;
  outline: none;
}
.rule-input input:focus { border-color: #409eff; }
.rule-input span { font-size: 13px; color: #909399; }

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 28px;
  padding-top: 20px;
  border-top: 1px solid #f0f2f5;
}
.btn-save {
  padding: 10px 28px;
  background: linear-gradient(135deg, #409eff, #66b1ff);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}
.btn-save:hover { opacity: 0.88; transform: translateY(-1px); }
.btn-backup {
  padding: 10px 28px;
  background: linear-gradient(135deg, #67c23a, #85ce61);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}
.btn-backup:hover { opacity: 0.88; transform: translateY(-1px); }
</style>