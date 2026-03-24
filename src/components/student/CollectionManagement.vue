<template>
  <div class="page-container">
    <h2>收藏管理</h2>

    <div v-if="collections.length > 0" class="collection-grid">
      <div v-for="item in collections" :key="item.id" class="collection-card">
        <div class="card-top">
          <span class="type-tag">{{ item.resource?.type?.name || '未分类' }}</span>
          <span class="points-badge">💎 {{ item.resource?.points_required ?? 0 }} 积分</span>
        </div>
        <h3 class="card-title">{{ item.resource?.title || '未知资源' }}</h3>
        <p class="card-desc">{{ item.resource?.description || '暂无描述' }}</p>
        <div class="card-meta">
          <span>📥 {{ item.resource?.downloads ?? 0 }} 次下载</span>
          <span>🕐 {{ formatDate(item.collect_date) }}</span>
        </div>
        <div class="card-actions">
          <button @click="downloadResource(item.resource)" class="btn-download">下载</button>
          <button @click="uncollect(item)" class="btn-uncollect">取消收藏</button>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <div class="empty-icon">📚</div>
      <p class="empty-title">还没有收藏任何资源</p>
      <p class="empty-sub">去资源浏览页面收藏感兴趣的内容吧</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const collections = ref<any[]>([])

const formatDate = (d: string) => {
  if (!d) return ''
  return new Date(d).toLocaleDateString('zh-CN')
}

const fetchCollections = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('http://127.0.0.1:8000/api/courses/collections/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    collections.value = res.data
  } catch (e) {
    console.error('获取收藏列表失败', e)
  }
}

const uncollect = async (item: any) => {
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`http://127.0.0.1:8000/api/courses/uncollect/${item.id}/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    collections.value = collections.value.filter(c => c.id !== item.id)
  } catch (e) {
    alert('操作失败')
  }
}

const downloadResource = async (resource: any) => {
  if (!resource) return
  try {
    const token = localStorage.getItem('token')
    await axios.post(`http://127.0.0.1:8000/api/courses/${resource.id}/download/`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    })
    resource.downloads += 1
    alert('下载成功！')
  } catch (e: any) {
    alert(e.response?.data?.error || '下载失败')
  }
}

onMounted(fetchCollections)
</script>

<style scoped>
.page-container { padding: 24px; }
.page-container h2 { margin: 0 0 24px; font-size: 22px; color: #1a1a2e; }

.collection-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.collection-card {
  background: white;
  border-radius: 14px;
  padding: 22px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.collection-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.card-top { display: flex; justify-content: space-between; align-items: center; }
.type-tag {
  background: #ecf5ff;
  color: #409eff;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}
.points-badge { color: #e6a23c; font-size: 13px; font-weight: 500; }

.card-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1a1a2e;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.card-desc {
  margin: 0;
  font-size: 13px;
  color: #909399;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #c0c4cc;
  padding-top: 10px;
  border-top: 1px solid #f5f5f5;
}

.card-actions { display: flex; gap: 10px; }
.btn-download, .btn-uncollect {
  flex: 1;
  padding: 8px 0;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: opacity 0.2s;
}
.btn-download { background: #409eff; color: white; }
.btn-download:hover { opacity: 0.85; }
.btn-uncollect { background: #fef0f0; color: #f56c6c; border: 1px solid #fde2e2; }
.btn-uncollect:hover { background: #fde2e2; }

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: #c0c4cc;
}
.empty-icon { font-size: 64px; margin-bottom: 16px; }
.empty-title { font-size: 16px; color: #909399; margin: 0 0 8px; }
.empty-sub { font-size: 13px; margin: 0; }
</style>