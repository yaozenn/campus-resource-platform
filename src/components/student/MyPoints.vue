<template>
  <div class="page-container">
    <h2>我的积分</h2>

    <div class="points-hero">
      <div class="points-circle">
        <div class="points-value">{{ totalPoints }}</div>
        <div class="points-label">当前积分</div>
      </div>
      <div class="points-summary">
        <div class="summary-item">
          <span class="summary-num add">+{{ totalAdded }}</span>
          <span class="summary-desc">累计获得</span>
        </div>
        <div class="summary-divider"></div>
        <div class="summary-item">
          <span class="summary-num deduct">-{{ totalDeducted }}</span>
          <span class="summary-desc">累计消耗</span>
        </div>
      </div>
    </div>

    <div class="records-card">
      <h3 class="records-title">积分明细</h3>
      <div v-if="records.length > 0" class="record-list">
        <div v-for="record in records" :key="record.id" class="record-item">
          <div class="record-left">
            <span class="record-icon">{{ record.type === 'add' ? '💰' : '💸' }}</span>
            <div>
              <div class="record-reason">{{ record.reason }}</div>
              <div class="record-time">{{ formatDate(record.record_date) }}</div>
            </div>
          </div>
          <span :class="['record-points', record.type]">
            {{ record.type === 'add' ? '+' : '-' }}{{ record.points }}
          </span>
        </div>
      </div>
      <div v-else class="empty-state">
        <div class="empty-icon">📋</div>
        <p>暂无积分记录</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const totalPoints = ref(0)
const records = ref<any[]>([])

const totalAdded = computed(() =>
  records.value.filter(r => r.type === 'add').reduce((s, r) => s + r.points, 0)
)
const totalDeducted = computed(() =>
  records.value.filter(r => r.type === 'deduct').reduce((s, r) => s + r.points, 0)
)

const formatDate = (d: string) => new Date(d).toLocaleString('zh-CN')

onMounted(async () => {
  const userStr = localStorage.getItem('user')
  if (userStr) totalPoints.value = JSON.parse(userStr).points || 0

  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('http://127.0.0.1:8000/api/points/user/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    totalPoints.value = res.data.total_points
    records.value = res.data.records
  } catch (e) {
    console.error('获取积分记录失败', e)
  }
})
</script>

<style scoped>
.page-container { padding: 24px; }
.page-container h2 { margin: 0 0 24px; font-size: 22px; color: #1a1a2e; }

.points-hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 36px 40px;
  display: flex;
  align-items: center;
  gap: 48px;
  margin-bottom: 28px;
  color: white;
  box-shadow: 0 8px 24px rgba(102,126,234,0.35);
}
.points-circle {
  text-align: center;
  background: rgba(255,255,255,0.15);
  border-radius: 50%;
  width: 140px;
  height: 140px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 3px solid rgba(255,255,255,0.3);
  flex-shrink: 0;
}
.points-value { font-size: 44px; font-weight: 700; line-height: 1; }
.points-label { font-size: 13px; opacity: 0.85; margin-top: 6px; }

.points-summary { display: flex; align-items: center; gap: 40px; }
.summary-item { text-align: center; }
.summary-num { display: block; font-size: 32px; font-weight: 700; }
.summary-num.add { color: #a8f0c6; }
.summary-num.deduct { color: #ffb3b3; }
.summary-desc { font-size: 13px; opacity: 0.85; margin-top: 4px; display: block; }
.summary-divider { width: 1px; height: 50px; background: rgba(255,255,255,0.25); }

.records-card {
  background: white;
  border-radius: 16px;
  padding: 28px 32px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.records-title { margin: 0 0 20px; font-size: 16px; color: #303133; }

.record-list { display: flex; flex-direction: column; gap: 4px; }
.record-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  border-radius: 10px;
  transition: background 0.15s;
}
.record-item:hover { background: #f8f9fc; }
.record-left { display: flex; align-items: center; gap: 14px; }
.record-icon { font-size: 24px; }
.record-reason { font-size: 14px; color: #303133; font-weight: 500; }
.record-time { font-size: 12px; color: #909399; margin-top: 3px; }
.record-points { font-size: 18px; font-weight: 700; }
.record-points.add { color: #67c23a; }
.record-points.deduct { color: #f56c6c; }

.empty-state { text-align: center; padding: 48px 20px; color: #c0c4cc; }
.empty-icon { font-size: 48px; margin-bottom: 12px; }
.empty-state p { margin: 0; font-size: 14px; }
</style>