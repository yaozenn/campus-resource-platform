<template>
  <div class="page-container">
    <h2>系统管理</h2>
    <div class="management-grid">
      <div class="management-card" @click="navigateTo('SystemSettings')">
        <div class="card-icon settings-icon">⚙️</div>
        <h3>系统设置</h3>
        <p>网站配置、安全设置等</p>
      </div>
      
      <div class="management-card" @click="navigateTo('TypeManagement')">
        <div class="card-icon type-icon">📚</div>
        <h3>资源类型管理</h3>
        <p>管理资源分类</p>
      </div>
      
      <div class="management-card" @click="navigateTo('ForumManagement')">
        <div class="card-icon forum-icon">💬</div>
        <h3>论坛管理</h3>
        <p>管理论坛帖子</p>
      </div>
      
      <div class="management-card" @click="navigateTo('AnnouncementManagement')">
        <div class="card-icon announcement-icon">📢</div>
        <h3>公告管理</h3>
        <p>发布和管理公告</p>
      </div>
      
      <div class="management-card" @click="navigateTo('DataAnalysis')">
        <div class="card-icon analysis-icon">📊</div>
        <h3>数据分析</h3>
        <p>系统数据统计</p>
      </div>
      
      <div class="management-card" @click="navigateTo('PointsManagement')">
        <div class="card-icon points-icon">🎁</div>
        <h3>积分管理</h3>
        <p>用户积分和奖品管理</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateTo = (component: string) => {
  const routeMap: Record<string, string> = {
    'SystemSettings': 'system',
    'TypeManagement': 'types',
    'ForumManagement': 'forum',
    'AnnouncementManagement': 'announcements',
    'DataAnalysis': 'analysis',
    'PointsManagement': 'points'
  }
  const route = routeMap[component] || component.toLowerCase()
  router.push(`/admin/${route}`)
}
</script>

<style scoped>
.page-container { padding: 20px; }
.management-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 30px; }
.management-card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); cursor: pointer; transition: all 0.3s ease; border: 2px solid transparent; }
.management-card:hover { transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.15); border-color: #409eff; }
.card-icon { font-size: 48px; margin-bottom: 20px; }
.management-card h3 { margin: 0 0 10px; color: #333; font-size: 18px; }
.management-card p { margin: 0; color: #666; font-size: 14px; line-height: 1.5; }

/* 不同卡片的图标样式 */
.settings-icon { color: #1890ff; }
.type-icon { color: #52c41a; }
.forum-icon { color: #faad14; }
.announcement-icon { color: #f5222d; }
.analysis-icon { color: #722ed1; }
.points-icon { color: #13c2c2; }
</style>
