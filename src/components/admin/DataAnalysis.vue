<template>
  <div class="page-container">
    <h2>
      <IconClipboard class="header-icon" />
      数据分析
    </h2>

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

      <div class="chart-card">
        <h3 class="chart-title">资源分类柱状图</h3>
        <div class="vertical-bar-chart">
          <div class="v-grid-lines">
            <div class="v-grid-line"></div>
            <div class="v-grid-line"></div>
            <div class="v-grid-line"></div>
            <div class="v-grid-line"></div>
          </div>
          
          <div class="v-bars-container">
            <div v-for="(seg, i) in resourceTypeSegments" :key="i" class="v-bar-item">
              <div class="v-bar-value" :style="{ color: seg.color }">{{ seg.count }}</div>
              <div class="v-bar-track">
                <div
                  class="v-bar-fill"
                  :style="{ height: Math.max(seg.pct, 2) + '%', background: seg.color }"
                ></div>
              </div>
              <div class="v-bar-label">{{ seg.name }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { IconUsers, IconBookOpen, IconMessageCircle, IconGift, IconClipboard } from '@/components/icons'

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
    { name: '文档', count: resourceTypeDistribution.value.document, color: '#10b981' },
    { name: '课程', count: resourceTypeDistribution.value.course, color: '#f59e0b' },
    { name: '其他', count: resourceTypeDistribution.value.other, color: '#8b5cf6' },
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
      
      if (data.resourceTypeDistribution) {
        resourceTypeDistribution.value = data.resourceTypeDistribution
      }
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
.page-container h2 { margin: 0 0 var(--spacing-lg); font-size: var(--font-size-2xl); font-weight: 600; color: var(--text-primary); font-family: var(--font-sf); }

/* 统计卡片 */
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--spacing-md); margin-bottom: var(--spacing-lg); }
.stat-card { background: var(--bg-primary); border-radius: var(--border-radius-lg); padding: var(--spacing-lg); display: flex; align-items: center; gap: var(--spacing-md); box-shadow: var(--shadow-sm); border: 1px solid var(--border-light); border-left: 4px solid transparent; transition: all var(--transition-normal); cursor: pointer; }
.stat-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
.stat-card.primary { border-left-color: var(--primary-color); }
.stat-card.success { border-left-color: var(--success-color); }
.stat-card.warning { border-left-color: var(--warning-color); }
.stat-card.danger { border-left-color: var(--error-color); }
.stat-icon { width: 48px; height: 48px; display: flex; align-items: center; justify-content: center; border-radius: 12px; background: rgba(13, 148, 136, 0.1); }
.stat-card.primary .stat-icon { background: rgba(13, 148, 136, 0.15); }
.stat-card.success .stat-icon { background: rgba(16, 185, 129, 0.15); }
.stat-card.warning .stat-icon { background: rgba(245, 158, 11, 0.15); }
.stat-card.danger .stat-icon { background: rgba(239, 68, 68, 0.15); }
.icon-svg { width: 24px; height: 24px; color: var(--primary-color); }
.stat-card.primary .icon-svg { color: var(--primary-color); }
.stat-card.success .icon-svg { color: var(--success-color); }
.stat-card.warning .icon-svg { color: var(--warning-color); }
.stat-card.danger .icon-svg { color: var(--error-color); }
.header-icon { width: 28px; height: 28px; color: var(--primary-color); margin-right: 10px; vertical-align: middle; }
.stat-num { font-size: 30px; font-weight: 700; color: var(--text-primary); line-height: 1; font-family: var(--font-sf); }
.stat-label { font-size: var(--font-size-sm); color: var(--text-secondary); margin-top: 6px; }

/* 图表行 */
.charts-row { display: grid; grid-template-columns: 1fr 1fr; gap: var(--spacing-md); margin-bottom: var(--spacing-md); }
.chart-card { background: var(--bg-primary); border-radius: var(--border-radius-lg); padding: var(--spacing-lg); border: 1px solid var(--border-light); box-shadow: var(--shadow-sm); transition: box-shadow var(--transition-normal); }
.chart-card:hover { box-shadow: var(--shadow-md); }
.chart-title { margin: 0 0 var(--spacing-lg); font-size: 16px; font-weight: 600; color: var(--text-primary); font-family: var(--font-sf); }

/* 饼图 */
.pie-wrap { display: flex; align-items: center; justify-content: center; gap: 30px; height: 200px; }
.pie-svg { width: 160px; height: 160px; flex-shrink: 0; }
.pie-center-num { font-size: 24px; font-weight: 700; fill: var(--text-primary); font-family: var(--font-sf); }
.pie-center-label { font-size: 12px; fill: var(--text-secondary); }
.pie-legend { display: flex; flex-direction: column; gap: 12px; }
.legend-row { display: flex; align-items: center; gap: 10px; }
.legend-dot { width: 12px; height: 12px; border-radius: 3px; flex-shrink: 0; }
.legend-name { width: 60px; font-size: 14px; color: var(--text-secondary); }
.legend-count { width: 40px; font-size: 14px; font-weight: 600; color: var(--text-primary); }
.legend-pct { font-size: 12px; color: var(--text-tertiary); text-align: right; width: 40px; }

/* 基础条形图(热门资源) */
.bar-list { display: flex; flex-direction: column; gap: 16px; height: 200px; justify-content: center; }
.bar-item { display: flex; align-items: center; gap: 12px; }
.bar-rank { width: 24px; height: 24px; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; flex-shrink: 0; color: white; background: var(--text-tertiary); }
.bar-rank.rank-1 { background: #f59e0b; }
.bar-rank.rank-2 { background: #9ca3af; }
.bar-rank.rank-3 { background: #b45309; }
.bar-info { flex: 1; }
.bar-name { font-size: 14px; color: var(--text-primary); margin-bottom: 6px; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 200px; }
.bar-track { height: 8px; background: var(--bg-tertiary); border-radius: 4px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 4px; transition: width 0.6s ease; }
.bar-value { font-size: 14px; font-weight: 600; color: var(--text-primary); min-width: 40px; text-align: right; }
.bar-unit { font-size: 12px; color: var(--text-tertiary); margin-left: 2px; font-weight: 400; }
.empty-tip { text-align: center; color: var(--text-tertiary); padding: 20px; }


/* ---------------- 新增：垂直柱状图样式 ---------------- */
.vertical-bar-chart {
  position: relative;
  height: 200px;
  width: 100%;
  display: flex;
  flex-direction: column;
}

/* 虚线背景网格 */
.v-grid-lines {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 24px; /* 留出底部标签空间 */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  z-index: 1;
}
.v-grid-line {
  border-top: 1px dashed var(--border-color);
  width: 100%;
}

/* 柱子容器区 */
.v-bars-container {
  position: relative;
  z-index: 2;
  flex: 1;
  display: flex;
  justify-content: space-around;
  align-items: flex-end;
  border-bottom: 1px solid var(--border-dark);
  padding-bottom: 4px; /* 柱子和底线的间距 */
  margin-bottom: 24px; /* 为底部文字预留位置 */
}

/* 单个垂直柱子项目 */
.v-bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  height: 100%; /* 撑满容器高度 */
  position: relative;
}

/* 顶部数值 */
.v-bar-value {
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 8px;
}

/* 柱子轨道（控制最大高度和底色） */
.v-bar-track {
  width: 36px;
  height: 140px; /* 图表中柱子可达到的最大高度 */
  background: var(--bg-tertiary);
  border-radius: 6px 6px 0 0;
  display: flex;
  align-items: flex-end; /* 从底部开始填充 */
  overflow: hidden;
}

/* 柱子填充（动画高度） */
.v-bar-fill {
  width: 100%;
  border-radius: 6px 6px 0 0;
  transition: height 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 底部标签名称 */
.v-bar-label {
  position: absolute;
  bottom: -26px; /* 放在底线下方 */
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 500;
  white-space: nowrap;
}
</style>