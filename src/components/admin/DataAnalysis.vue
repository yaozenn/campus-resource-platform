<template>
  <div class="page-container">
    <h2>数据分析</h2>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card blue">
        <div class="stat-icon">👥</div>
        <div class="stat-body">
          <div class="stat-num">{{ stats.totalUsers }}</div>
          <div class="stat-label">用户总数</div>
        </div>
      </div>
      <div class="stat-card green">
        <div class="stat-icon">📚</div>
        <div class="stat-body">
          <div class="stat-num">{{ stats.totalCourses }}</div>
          <div class="stat-label">资源总数</div>
        </div>
      </div>
      <div class="stat-card orange">
        <div class="stat-icon">💬</div>
        <div class="stat-body">
          <div class="stat-num">{{ stats.totalPosts }}</div>
          <div class="stat-label">论坛帖子</div>
        </div>
      </div>
      <div class="stat-card purple">
        <div class="stat-icon">🎯</div>
        <div class="stat-body">
          <div class="stat-num">{{ stats.pendingCourses }}</div>
          <div class="stat-label">待审核资源</div>
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

    <!-- 积分分布 -->
    <div class="chart-card full-width">
      <h3 class="chart-title">积分概览</h3>
      <div class="points-overview">
        <div class="points-stat-item">
          <div class="ps-num">{{ stats.totalPoints }}</div>
          <div class="ps-label">全平台积分总量</div>
        </div>
        <div class="points-stat-item">
          <div class="ps-num">{{ avgPoints }}</div>
          <div class="ps-label">人均积分</div>
        </div>
        <div class="points-stat-item">
          <div class="ps-num">{{ stats.totalUsers }}</div>
          <div class="ps-label">参与用户数</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

const stats = ref({
  totalUsers: 0,
  totalCourses: 0,
  totalPosts: 0,
  totalPoints: 0,
  pendingCourses: 0
})

const userDistribution = ref({ students: 0, teachers: 0, admins: 0 })
const topCourses = ref<any[]>([])

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

onMounted(fetchStats)
</script>

<style scoped>
.page-container { padding: 24px; }
.page-container h2 { margin: 0 0 24px; font-size: 22px; color: #1a1a2e; }

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}
.stat-card {
  background: white;
  border-radius: 14px;
  padding: 22px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  border-left: 4px solid transparent;
  transition: transform 0.2s;
}
.stat-card:hover { transform: translateY(-2px); }
.stat-card.blue { border-left-color: #409eff; }
.stat-card.green { border-left-color: #67c23a; }
.stat-card.orange { border-left-color: #e6a23c; }
.stat-card.purple { border-left-color: #9b59b6; }
.stat-icon { font-size: 36px; }
.stat-num { font-size: 30px; font-weight: 700; color: #1a1a2e; line-height: 1; }
.stat-label { font-size: 13px; color: #909399; margin-top: 6px; }

/* 图表行 */
.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}
.chart-card {
  background: white;
  border-radius: 14px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.chart-card.full-width { grid-column: 1 / -1; }
.chart-title { margin: 0 0 20px; font-size: 15px; font-weight: 600; color: #303133; }

/* 饼图 */
.pie-wrap { display: flex; align-items: center; gap: 28px; }
.pie-svg { width: 180px; height: 180px; flex-shrink: 0; }
.pie-center-num { font-size: 22px; font-weight: 700; fill: #1a1a2e; }
.pie-center-label { font-size: 11px; fill: #909399; }
.pie-legend { display: flex; flex-direction: column; gap: 12px; flex: 1; }
.legend-row { display: flex; align-items: center; gap: 8px; }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.legend-name { flex: 1; font-size: 13px; color: #606266; }
.legend-count { font-size: 13px; font-weight: 600; color: #303133; }
.legend-pct { font-size: 12px; color: #c0c4cc; min-width: 36px; text-align: right; }

/* 条形图 */
.bar-list { display: flex; flex-direction: column; gap: 14px; }
.bar-item { display: flex; align-items: center; gap: 12px; }
.bar-rank {
  width: 24px; height: 24px; border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 700; flex-shrink: 0; color: white;
  background: #c0c4cc;
}
.bar-rank.rank-1 { background: #f7ba2a; }
.bar-rank.rank-2 { background: #b0b0b0; }
.bar-rank.rank-3 { background: #cd7f32; }
.bar-info { flex: 1; }
.bar-name { font-size: 13px; color: #303133; margin-bottom: 6px; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 200px; }
.bar-track { height: 8px; background: #f4f6fb; border-radius: 4px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 4px; transition: width 0.6s ease; }
.bar-value { font-size: 14px; font-weight: 600; color: #303133; min-width: 50px; text-align: right; }
.bar-unit { font-size: 11px; color: #909399; margin-left: 2px; }
.empty-tip { text-align: center; color: #c0c4cc; padding: 20px; }

/* 积分概览 */
.points-overview { display: flex; gap: 0; }
.points-stat-item {
  flex: 1;
  text-align: center;
  padding: 20px;
  border-right: 1px solid #f0f2f5;
}
.points-stat-item:last-child { border-right: none; }
.ps-num { font-size: 32px; font-weight: 700; color: #e6a23c; line-height: 1; }
.ps-label { font-size: 13px; color: #909399; margin-top: 8px; }
</style>