<template>
  <div class="page-container">
    <h2>
      <IconSettings class="header-icon" />
      系统管理
    </h2>
    <div class="management-grid">
      <div class="management-card" @click="navigateTo('SystemSettings')">
        <div class="card-icon settings-icon">
          <IconSettings class="icon-svg" />
        </div>
        <h3>系统设置</h3>
        <p>网站配置、安全设置等</p>
      </div>
      
      <div class="management-card" @click="navigateTo('TypeManagement')">
        <div class="card-icon type-icon">
          <IconBookOpen class="icon-svg" />
        </div>
        <h3>资源类型管理</h3>
        <p>管理资源分类</p>
      </div>
      
      <div class="management-card" @click="navigateTo('ForumManagement')">
        <div class="card-icon forum-icon">
          <IconMessageCircle class="icon-svg" />
        </div>
        <h3>论坛管理</h3>
        <p>管理论坛帖子</p>
      </div>
      
      <div class="management-card" @click="navigateTo('AnnouncementManagement')">
        <div class="card-icon announcement-icon">
          <IconBell class="icon-svg" />
        </div>
        <h3>公告管理</h3>
        <p>发布和管理公告</p>
      </div>
      
      <div class="management-card" @click="navigateTo('DataAnalysis')">
        <div class="card-icon analysis-icon">
          <IconClipboard class="icon-svg" />
        </div>
        <h3>数据分析</h3>
        <p>系统数据统计</p>
      </div>
      
      <div class="management-card" @click="navigateTo('PointsManagement')">
        <div class="card-icon points-icon">
          <IconGift class="icon-svg" />
        </div>
        <h3>积分管理</h3>
        <p>用户积分和奖品管理</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { IconSettings, IconBookOpen, IconMessageCircle, IconBell, IconClipboard, IconGift } from '@/components/icons'

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
.page-container { padding: var(--spacing-lg); }
.page-container h2 { margin: 0 0 var(--spacing-lg); font-size: var(--h2-font-size); font-weight: var(--h2-font-weight); color: var(--text-primary); display: flex; align-items: center; }
.header-icon { width: 28px; height: 28px; color: var(--primary-color); margin-right: 10px; }
.management-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: var(--spacing-md); margin-top: var(--spacing-lg); }
.management-card { background: var(--bg-primary); padding: var(--spacing-lg); border-radius: var(--border-radius-lg); box-shadow: var(--shadow-md); cursor: pointer; transition: all var(--transition-normal); border: 2px solid transparent; }
.management-card:hover { transform: translateY(-5px); box-shadow: var(--shadow-lg); border-color: var(--primary-color); }
.card-icon { width: 56px; height: 56px; margin-bottom: var(--spacing-md); display: flex; align-items: center; justify-content: center; border-radius: 12px; }
.icon-svg { width: 32px; height: 32px; }
.management-card h3 { margin: 0 0 var(--spacing-xs); color: var(--text-primary); font-size: var(--font-size-lg); font-weight: var(--font-weight-semibold); }
.management-card p { margin: 0; color: var(--text-secondary); font-size: var(--font-size-base); line-height: 1.5; }

/* 不同卡片的图标样式 */
.settings-icon { background: rgba(24, 144, 255, 0.1); color: #1890ff; }
.type-icon { background: rgba(82, 196, 26, 0.1); color: #52c41a; }
.forum-icon { background: rgba(250, 173, 20, 0.1); color: #faad14; }
.announcement-icon { background: rgba(245, 34, 45, 0.1); color: #f5222d; }
.analysis-icon { background: rgba(114, 46, 209, 0.1); color: #722ed1; }
.points-icon { background: rgba(19, 194, 194, 0.1); color: #13c2c2; }
</style>
