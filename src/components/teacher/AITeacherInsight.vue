<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <h2>智能教学助手</h2>
        <span class="beta-tag">AI 驱动</span>
      </div>
      <button @click="fetchInsight" class="btn-refresh" :disabled="loading">
        <IconRefresh v-if="!loading" class="btn-icon" />
        <span v-if="loading">分析中...</span>
        <span v-else>重新分析</span>
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-card">
      <div class="loading-dots">
        <span></span><span></span><span></span>
      </div>
      <p>AI 正在分析您的课程数据，请稍候...</p>
    </div>

    <!-- AI 建议卡片 -->
    <div v-else-if="insight" class="insight-card">
      <div class="insight-header">
        <div class="ai-avatar">
          <IconSettings class="ai-icon" />
        </div>
        <div>
          <div class="ai-name">教学顾问 AI</div>
          <div class="ai-time">{{ currentTime }}</div>
        </div>
      </div>
      <div class="insight-content">{{ insight }}</div>
      <div class="insight-footer">
        <span class="footer-tip">
          <IconInfo class="tip-icon" />
          建议基于您的课程数据实时生成，每次点击「重新分析」可获取新建议
        </span>
      </div>
    </div>

    <!-- 课程数据概览 -->
    <div v-if="stats.length > 0" class="stats-section">
      <h3 class="section-title">
        <IconCollection class="section-icon" />
        课程数据概览
      </h3>
      <div class="stats-grid">
        <div v-for="course in stats" :key="course.id" class="stat-card">
          <div class="stat-card-header">
            <span class="course-title">{{ course.title }}</span>
            <span :class="['status-tag', course.status]">{{ statusText(course.status) }}</span>
          </div>
          <div class="stat-numbers">
            <div class="stat-item">
              <div class="stat-num">{{ course.downloads }}</div>
              <div class="stat-label">下载次数</div>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <div class="stat-num">{{ course.comment_count }}</div>
              <div class="stat-label">评论数量</div>
            </div>
          </div>
          <div v-if="course.recent_comments && course.recent_comments.length > 0" class="recent-comments">
            <div class="comments-label">最近评论：</div>
            <div v-for="(c, i) in course.recent_comments.slice(0, 2)" :key="i" class="comment-preview">
              "{{ c }}"
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="!loading && !insight" class="empty-state">
      <IconBook class="empty-icon" />
      <p class="empty-title">点击「重新分析」获取您的教学建议</p>
      <p class="empty-sub">AI 将根据您的课程数据生成个性化建议</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { IconRefresh, IconSettings, IconInfo, IconCollection, IconBook } from '../../components/icons'

const insight = ref('')
const stats = ref<any[]>([])
const loading = ref(false)
const currentTime = ref('')

const statusText = (s: string) => {
  const map: any = { active: '已发布', pending: '待审核', rejected: '已拒绝' }
  return map[s] || s
}

const fetchInsight = async () => {
  loading.value = true
  insight.value = ''
  stats.value = []
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('http://127.0.0.1:8000/api/ai/teacher-insight/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    insight.value = res.data.insight
    stats.value = res.data.stats || []
    currentTime.value = new Date().toLocaleString('zh-CN')
  } catch (e) {
    insight.value = '获取建议失败，请检查网络连接后重试。'
  } finally {
    loading.value = false
  }
}

onMounted(fetchInsight)
</script>

<style scoped>
.page-container { padding: 24px; }

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.header-left { display: flex; align-items: center; gap: 12px; }
.page-header h2 { margin: 0; font-size: 22px; color: var(--text-primary); font-family: var(--font-sf); }
.beta-tag {
  padding: 3px 10px;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  color: white;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
}
.btn-refresh {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all var(--transition-fast);
}
.btn-refresh:hover { background: var(--primary-dark); }
.btn-refresh:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-icon { width: 16px; height: 16px; }

/* 加载 */
.loading-card {
  background: white;
  border-radius: var(--border-radius-xl);
  padding: 48px;
  text-align: center;
  box-shadow: var(--shadow-md);
  margin-bottom: 24px;
  border: 1px solid var(--border-light);
}
.loading-dots { display: flex; justify-content: center; gap: 8px; margin-bottom: 16px; }
.loading-dots span {
  width: 10px; height: 10px;
  background: var(--primary-color);
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}
.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }
@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}
.loading-card p { color: var(--text-secondary); font-size: 14px; margin: 0; }

/* AI 建议卡片 */
.insight-card {
  background: white;
  border-radius: var(--border-radius-xl);
  padding: 24px 28px;
  box-shadow: var(--shadow-md);
  margin-bottom: 24px;
  border-left: 4px solid var(--primary-color);
  border: 1px solid var(--border-light);
}
.insight-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 16px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--border-light);
}
.ai-avatar {
  background: rgba(13, 148, 136, 0.1);
  width: 52px; height: 52px;
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.ai-icon {
  width: 28px;
  height: 28px;
  color: var(--primary-color);
}
.ai-name { font-size: 15px; font-weight: 600; color: var(--text-primary); }
.ai-time { font-size: 12px; color: var(--text-tertiary); margin-top: 3px; }

.insight-content {
  font-size: 15px;
  color: var(--text-primary);
  line-height: 1.9;
  white-space: pre-wrap;
}

.insight-footer {
  margin-top: 16px;
  padding-top: 14px;
  border-top: 1px solid var(--border-light);
}
.footer-tip { 
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px; 
  color: var(--text-tertiary); 
}
.tip-icon {
  width: 14px;
  height: 14px;
}

/* 课程数据 */
.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 16px;
}
.section-icon {
  width: 20px;
  height: 20px;
  color: var(--primary-color);
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}
.stat-card {
  background: white;
  border-radius: var(--border-radius-lg);
  padding: 18px 20px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
}
.stat-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 14px;
  gap: 8px;
}
.course-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
  flex: 1;
}
.status-tag {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 20px;
  white-space: nowrap;
  flex-shrink: 0;
}
.status-tag.active { background: rgba(16, 185, 129, 0.1); color: #10b981; }
.status-tag.pending { background: rgba(245, 158, 11, 0.1); color: #f59e0b; }
.status-tag.rejected { background: rgba(239, 68, 68, 0.1); color: #ef4444; }

.stat-numbers {
  display: flex;
  align-items: center;
  gap: 0;
  margin-bottom: 12px;
  background: var(--bg-tertiary);
  border-radius: 10px;
  padding: 10px 0;
}
.stat-item { flex: 1; text-align: center; }
.stat-num { font-size: 24px; font-weight: 700; color: var(--text-primary); line-height: 1; font-family: var(--font-sf); }
.stat-label { font-size: 11px; color: var(--text-tertiary); margin-top: 4px; }
.stat-divider { width: 1px; height: 36px; background: var(--border-color); }

.recent-comments { }
.comments-label { font-size: 12px; color: var(--text-tertiary); margin-bottom: 6px; }
.comment-preview {
  font-size: 12px;
  color: var(--text-secondary);
  background: var(--bg-tertiary);
  padding: 6px 10px;
  border-radius: 6px;
  margin-bottom: 4px;
  border-left: 2px solid var(--border-color);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-tertiary);
}
.empty-icon { 
  width: 64px; 
  height: 64px; 
  margin: 0 auto 16px; 
  color: var(--text-tertiary);
}
.empty-title { font-size: 16px; color: var(--text-secondary); margin: 0 0 8px; }
.empty-sub { font-size: 13px; margin: 0; }
</style>
