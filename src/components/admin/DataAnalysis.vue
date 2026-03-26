<template>
  <div class="page-container">
    <h2>
      <IconClipboard class="header-icon" />
      数据分析
    </h2>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card primary" @click="goToUserOverview">
        <div class="stat-icon">
          <IconUsers class="icon-svg" />
        </div>
        <div class="stat-body">
          <div class="stat-num">{{ stats.totalUsers }}</div>
          <div class="stat-label">用户总数</div>
        </div>
      </div>
      <div class="stat-card success" @click="goToResourceOverview">
        <div class="stat-icon">
          <IconBookOpen class="icon-svg" />
        </div>
        <div class="stat-body">
          <div class="stat-num">{{ stats.totalCourses }}</div>
          <div class="stat-label">资源总数</div>
        </div>
      </div>
      <div class="stat-card warning" @click="goToForumOverview">
        <div class="stat-icon">
          <IconMessageCircle class="icon-svg" />
        </div>
        <div class="stat-body">
          <div class="stat-num">{{ stats.totalPosts }}</div>
          <div class="stat-label">论坛帖子</div>
        </div>
      </div>
      <div class="stat-card danger">
        <div class="stat-icon">
          <IconGift class="icon-svg" />
        </div>
        <div class="stat-body">
          <div class="stat-num">{{ stats.totalPoints }}</div>
          <div class="stat-label">积分总量</div>
        </div>
      </div>
    </div>

    <div class="charts-row">
      <!-- 用户分布饼图 -->
      <div class="chart-card">
        <h3 class="chart-title">用户角色分布</h3>
        <div class="pie-wrap">
          <svg viewBox="0 0 200 200" class="pie-svg">
            <circle
              v-for="(seg, i) in pieSegments"
              :key="i"
              cx="100" cy="100" r="70"
              fill="none"
              :stroke="seg.color"
              stroke-width="40"
              :stroke-dasharray="`${seg.dash} ${circumference}`"
              :stroke-dashoffset="-seg.offset"
              transform="rotate(-90 100 100)"
            />
            <circle cx="100" cy="100" r="50" fill="white" />
            <text x="100" y="96" text-anchor="middle" class="pie-center-num">{{ stats.totalUsers }}</text>
            <text x="100" y="112" text-anchor="middle" class="pie-center-label">总用户</text>
          </svg>
          <div class="pie-legend">
            <div v-for="(seg, i) in pieSegments" :key="i" class="legend-row">
              <span class="legend-dot" :style="{ background: seg.color }"></span>
              <span class="legend-name">{{ seg.name }}</span>
              <span class="legend-count">{{ seg.count }} 人</span>
              <span class="legend-pct">{{ seg.pct }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 热门资源 -->
      <div class="chart-card">
        <h3 class="chart-title">热门资源 TOP 5</h3>
        <div class="bar-list">
          <div v-for="(course, i) in topCourses" :key="course.id" class="bar-item">
            <div class="bar-rank" :class="`rank-${i+1}`">{{ i + 1 }}</div>
            <div class="bar-info">
              <div class="bar-name">{{ course.title }}</div>
              <div class="bar-track">
                <div
                  class="bar-fill"
                  :style="{ width: barWidth(course.downloads) + '%', background: barColor(i) }"
                ></div>
              </div>
            </div>
            <div class="bar-value">{{ course.downloads }}<span class="bar-unit">次</span></div>
          </div>
          <div v-if="topCourses.length === 0" class="empty-tip">暂无数据</div>
        </div>
      </div>
    </div>

    <div class="charts-row">
      <!-- 资源类型分布 -->
      <div class="chart-card">
        <h3 class="chart-title">资源类型分布</h3>
        <div class="pie-wrap">
          <svg viewBox="0 0 200 200" class="pie-svg">
            <circle
              v-for="(seg, i) in resourceTypeSegments"
              :key="i"
              cx="100" cy="100" r="70"
              fill="none"
              :stroke="seg.color"
              stroke-width="40"
              :stroke-dasharray="`${seg.dash} ${circumference}`"
              :stroke-dashoffset="-seg.offset"
              transform="rotate(-90 100 100)"
            />
            <circle cx="100" cy="100" r="50" fill="white" />
            <text x="100" y="96" text-anchor="middle" class="pie-center-num">{{ stats.totalCourses }}</text>
            <text x="100" y="112" text-anchor="middle" class="pie-center-label">总资源</text>
          </svg>
          <div class="pie-legend">
            <div v-for="(seg, i) in resourceTypeSegments" :key="i" class="legend-row">
              <span class="legend-dot" :style="{ background: seg.color }"></span>
              <span class="legend-name">{{ seg.name }}</span>
              <span class="legend-count">{{ seg.count }} 个</span>
              <span class="legend-pct">{{ seg.pct }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 积分分布 -->
      <div class="chart-card">
        <h3 class="chart-title">积分概览</h3>
        <div class="points-overview">
          <div class="points-stat-item">
            <div class="ps-num">{{ stats.totalPoints }}</div>
            <div class="ps-label">全平台积分</div>
          </div>
          <div class="points-stat-item">
            <div class="ps-num">{{ avgPoints }}</div>
            <div class="ps-label">人均积分</div>
          </div>
          <div class="points-stat-item">
            <div class="ps-num">{{ stats.totalUsers }}</div>
            <div class="ps-label">参与用户</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { IconUsers, IconBookOpen, IconMessageCircle, IconGift, IconClipboard } from '../icons'

const router = useRouter()

const stats = ref({
  totalUsers: 0,
  totalCourses: 0,
  totalPosts: 0,
  totalPoints: 0
})

const userDistribution = ref({ students: 0, teachers: 0, admins: 0 })
const topCourses = ref<any[]>([])
const resourceTypeDistribution = ref({ video: 0, document: 0, course: 0, other: 0 })

const circumference = 2 * Math.PI * 70

const pieSegments = computed(() => {
  const total = stats.value.totalUsers || 1
  const items = [
    { name: '学生', count: userDistribution.value.students, color: '#409eff' },
    { name: '老师', count: userDistribution.value.teachers, color: '#67c23a' },
    { name: '管理员', count: userDistribution.value.admins, color: '#e6a23c' },
  ]
  let offset = 0
  return items.map(item => {
    const pct = Math.round((item.count / total) * 100)
    const dash = (item.count / total) * circumference
    const seg = { ...item, pct, dash, offset }
    offset += dash
    return seg
  })
})

const maxDownloads = computed(() => Math.max(...topCourses.value.map(c => c.downloads), 1))
const barWidth = (downloads: number) => Math.max((downloads / maxDownloads.value) * 100, 4)
const barColors = ['#409eff', '#67c23a', '#e6a23c', '#9b59b6', '#e74c3c']
const barColor = (i: number) => barColors[i] || '#409eff'

const avgPoints = computed(() => {
  if (!stats.value.totalUsers) return 0
  return Math.round(stats.value.totalPoints / stats.value.totalUsers)
})

const resourceTypeSegments = computed(() => {
  const total = stats.value.totalCourses || 1
  const items = [
    { name: '视频', count: resourceTypeDistribution.value.video, color: '#409eff' },
    { name: '文档', count: resourceTypeDistribution.value.document, color: '#67c23a' },
    { name: '课程', count: resourceTypeDistribution.value.course, color: '#e6a23c' },
    { name: '其他', count: resourceTypeDistribution.value.other, color: '#9b59b6' },
  ]
  let offset = 0
  return items.map(item => {
    const pct = Math.round((item.count / total) * 100)
    const dash = (item.count / total) * circumference
    const seg = { ...item, pct, dash, offset }
    offset += dash
    return seg
  })
})

const fetchStats = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/stats/')
    const data = await res.json()
    if (data.success) {
      stats.value = data.stats
      userDistribution.value = data.userDistribution
      topCourses.value = data.topCourses
    }
  } catch (e) {
    console.error('获取统计数据失败', e)
  }
}

const goToUserOverview = () => {
  router.push('/admin/user-overview')
}

const goToResourceOverview = () => {
  router.push('/admin/resource-overview')
}

const goToForumOverview = () => {
  router.push('/admin/forum-overview')
}

onMounted(fetchStats)
</script>

<style scoped>
.page-container { padding: var(--spacing-lg); }
.page-container h2 { margin: 0 0 var(--spacing-lg); font-size: var(--h2-font-size); font-weight: var(--h2-font-weight); color: var(--text-primary); }

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}
.stat-card {
  background: var(--bg-primary);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  box-shadow: var(--shadow-md);
  border-left: 4px solid transparent;
  transition: all var(--transition-normal);
  cursor: pointer;
}
.stat-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); }
.stat-card.primary { border-left-color: var(--primary-color); }
.stat-card.success { border-left-color: var(--success-color); }
.stat-card.warning { border-left-color: var(--warning-color); }
.stat-card.danger { border-left-color: var(--danger-color); }
.stat-icon { 
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: rgba(13, 148, 136, 0.1);
}
.stat-card.primary .stat-icon { background: rgba(13, 148, 136, 0.15); }
.stat-card.success .stat-icon { background: rgba(16, 185, 129, 0.15); }
.stat-card.warning .stat-icon { background: rgba(245, 158, 11, 0.15); }
.stat-card.danger .stat-icon { background: rgba(239, 68, 68, 0.15); }
.icon-svg { 
  width: 24px; 
  height: 24px; 
  color: var(--primary-color);
}
.stat-card.primary .icon-svg { color: var(--primary-color); }
.stat-card.success .icon-svg { color: var(--success-color); }
.stat-card.warning .icon-svg { color: var(--warning-color); }
.stat-card.danger .icon-svg { color: var(--danger-color); }
.header-icon {
  width: 28px;
  height: 28px;
  color: var(--primary-color);
  margin-right: 10px;
  vertical-align: middle;
}
.stat-num { font-size: 30px; font-weight: var(--font-weight-bold); color: var(--text-primary); line-height: 1; }
.stat-label { font-size: var(--font-size-sm); color: var(--text-placeholder); margin-top: 6px; }

/* 图表行 */
.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}
.chart-card {
  background: var(--bg-primary);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-md);
  transition: box-shadow var(--transition-normal);
}
.chart-card:hover { box-shadow: var(--shadow-lg); }
.chart-card.full-width { grid-column: 1 / -1; }
.chart-title { margin: 0 0 var(--spacing-md); font-size: var(--h4-font-size); font-weight: var(--h4-font-weight); color: var(--text-primary); }

/* 饼图 */
.pie-wrap { display: flex; align-items: center; gap: var(--spacing-lg); }
.pie-svg { width: 180px; height: 180px; flex-shrink: 0; }
.pie-center-num { font-size: 22px; font-weight: var(--font-weight-bold); fill: var(--text-primary); }
.pie-center-label { font-size: 11px; fill: var(--text-placeholder); }
.pie-legend { display: flex; flex-direction: column; gap: var(--spacing-sm); flex: 1; }
.legend-row { display: flex; align-items: center; gap: var(--spacing-xs); }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.legend-name { flex: 1; font-size: var(--font-size-sm); color: var(--text-secondary); }
.legend-count { font-size: var(--font-size-sm); font-weight: var(--font-weight-semibold); color: var(--text-primary); }
.legend-pct { font-size: var(--font-size-xs); color: var(--text-disabled); min-width: 36px; text-align: right; }

/* 条形图 */
.bar-list { display: flex; flex-direction: column; gap: var(--spacing-sm); }
.bar-item { display: flex; align-items: center; gap: var(--spacing-sm); }
.bar-rank {
  width: 24px; height: 24px; border-radius: var(--border-radius-sm);
  display: flex; align-items: center; justify-content: center;
  font-size: var(--font-size-xs); font-weight: var(--font-weight-bold); flex-shrink: 0; color: white;
  background: var(--text-disabled);
}
.bar-rank.rank-1 { background: #f7ba2a; }
.bar-rank.rank-2 { background: #b0b0b0; }
.bar-rank.rank-3 { background: #cd7f32; }
.bar-info { flex: 1; }
.bar-name { font-size: var(--font-size-sm); color: var(--text-primary); margin-bottom: 6px; font-weight: var(--font-weight-medium); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 200px; }
.bar-track { height: 8px; background: var(--bg-secondary); border-radius: var(--border-radius-sm); overflow: hidden; }
.bar-fill { height: 100%; border-radius: var(--border-radius-sm); transition: width 0.6s ease; }
.bar-value { font-size: var(--font-size-sm); font-weight: var(--font-weight-semibold); color: var(--text-primary); min-width: 50px; text-align: right; }
.bar-unit { font-size: var(--font-size-xs); color: var(--text-placeholder); margin-left: 2px; }
.empty-tip { text-align: center; color: var(--text-disabled); padding: var(--spacing-md); }

/* 积分概览 */
.points-overview { display: flex; gap: 0; }
.points-stat-item {
  flex: 1;
  text-align: center;
  padding: var(--spacing-md);
  border-right: 1px solid var(--border-light);
}
.points-stat-item:last-child { border-right: none; }
.ps-num { font-size: 32px; font-weight: var(--font-weight-bold); color: var(--warning-color); line-height: 1; }
.ps-label { font-size: var(--font-size-sm); color: var(--text-placeholder); margin-top: 8px; }
</style>