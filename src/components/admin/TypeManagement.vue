<template>
  <div class="page-container fade-in">
    <div class="page-header">
      <h2>资源分类体系总览</h2>
      <p class="subtitle">
        平台核心分类字典（由系统底层统一配置，为保证师生端数据一致性，当前已禁用手动增删）
      </p>
    </div>
    
    <div v-if="loading" class="loading-state">
      <p>正在加载分类数据...</p>
    </div>

    <div v-else class="category-grid">
      <div v-for="(subTypes, mainCategory) in groupedTypes" :key="mainCategory" class="category-card card">
        <div class="card-header">
          <div class="header-title">
            <span class="category-icon">{{ getCategoryIcon(String(mainCategory)) }}</span>
            <h3>{{ mainCategory }}</h3>
          </div>
          <span class="count-badge">{{ subTypes.length }} 个细分项</span>
        </div>
        
        <div class="card-body">
          <div class="tags-container">
            <div v-for="type in subTypes" :key="type.id" class="type-tag">
              {{ type.name }}
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="!loading && Object.keys(groupedTypes).length === 0" class="empty-state card">
      <p>暂无分类数据，请联系超级管理员运行初始化脚本</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const types = ref<any[]>([])
const loading = ref(true)

// 根据 description（大类名）对类型进行分组
const groupedTypes = computed(() => {
  const groups: Record<string, any[]> = {}
  types.value.forEach(t => {
    // 如果没有 description，归为"其他未分类"
    const main = t.description || '其他未分类'
    if (!groups[main]) {
      groups[main] = []
    }
    groups[main].push(t)
  })
  return groups
})

// 为不同的大类分配简单的 Emoji 图标
const getCategoryIcon = (category: string) => {
  if (category.includes('课程')) return '📚'
  if (category.includes('网络')) return '🌐'
  if (category.includes('书籍')) return '📖'
  return '📁'
}

const fetchTypes = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/courses/types/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    types.value = response.data
  } catch (error) {
    console.error('获取课程类型失败', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchTypes()
})
</script>

<style scoped>
.page-container {
  padding: var(--spacing-lg);
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: var(--spacing-lg);
}

.page-header h2 {
  font-size: var(--font-size-2xl);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
  font-family: var(--font-sf);
}

.subtitle {
  color: var(--warning-color);
  font-size: var(--font-size-sm);
  background: rgba(245, 158, 11, 0.1);
  padding: 8px 16px;
  border-radius: var(--border-radius-md);
  display: inline-block;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-tertiary);
  font-size: var(--font-size-base);
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: var(--spacing-lg);
}

.card {
  background: var(--bg-primary);
  border-radius: var(--border-radius-xl);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
  transition: all var(--transition-normal);
  overflow: hidden;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-light);
}

.card-header {
  padding: var(--spacing-lg);
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.category-icon {
  font-size: 24px;
}

.card-header h3 {
  margin: 0;
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-primary);
}

.count-badge {
  background: var(--primary-soft);
  color: var(--primary-dark);
  padding: 4px 12px;
  border-radius: var(--border-radius-full);
  font-size: var(--font-size-xs);
  font-weight: 600;
}

.card-body {
  padding: var(--spacing-lg);
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.type-tag {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  padding: 8px 16px;
  border-radius: var(--border-radius-lg);
  font-size: var(--font-size-sm);
  font-weight: 500;
  border: 1px solid var(--border-color);
  transition: all var(--transition-fast);
}

.type-tag:hover {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.fade-in {
  animation: fadeIn var(--transition-normal);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>