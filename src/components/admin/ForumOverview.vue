<template>
  <div class="page-container">
    <div class="page-header">
      <button @click="goBack" class="btn-back">
        <IconArrowLeft class="btn-icon" />
        返回数据分析
      </button>
      <h2>
        <IconMessageCircle class="header-icon" />
        论坛帖子总览
      </h2>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-summary">
      <div class="summary-card">
        <div class="summary-icon"><IconMessageCircle class="icon-svg" /></div>
        <div class="summary-value">{{ totalPosts }}</div>
        <div class="summary-label">总帖子数</div>
      </div>
      <div class="summary-card">
        <div class="summary-icon"><IconMessage class="icon-svg" /></div>
        <div class="summary-value">{{ totalComments }}</div>
        <div class="summary-label">总评论数</div>
      </div>
      <div class="summary-card">
        <div class="summary-icon"><IconFlame class="icon-svg" /></div>
        <div class="summary-value">{{ activePosts }}</div>
        <div class="summary-label">活跃帖子</div>
      </div>
      <div class="summary-card">
        <div class="summary-icon"><IconUser class="icon-svg" /></div>
        <div class="summary-value">{{ topPostAuthor }}</div>
        <div class="summary-label">最高产作者</div>
      </div>
    </div>

    <!-- 帖子列表 -->
    <div class="post-section">
      <h3>帖子列表</h3>
      <div class="filter-bar">
        <input v-model="searchText" placeholder="搜索帖子标题..." class="search-input" />
      </div>
      
      <div class="post-list">
        <div v-for="post in filteredPosts" :key="post.id" class="post-card">
          <div class="post-title">{{ post.title }}</div>
          <div class="post-meta">
            <span><IconUserCircle class="meta-icon-svg" /> {{ post.author?.name || post.author?.username || '未知' }}</span>
            <span><IconCalendar class="meta-icon-svg" /> {{ formatTime(post.post_date) }}</span>
            <span><IconMessage class="meta-icon-svg" /> {{ post.comment_count || 0 }} 评论</span>
          </div>
          <div class="post-content">{{ post.content }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { formatTime } from '../../utils/timeFormat'
import { IconMessageCircle, IconMessage, IconFlame, IconUser, IconArrowLeft, IconUserCircle, IconCalendar } from '../icons'

const router = useRouter()
const posts = ref<any[]>([])
const searchText = ref('')

const totalPosts = computed(() => posts.value.length)
const totalComments = computed(() => posts.value.reduce((sum, p) => sum + (p.comment_count || 0), 0))
const activePosts = computed(() => posts.value.filter(p => p.comment_count > 0).length)
const topPostAuthor = computed(() => {
  const authorCount: any = {}
  posts.value.forEach(p => {
    const author = p.author?.name || p.author?.username || '未知'
    authorCount[author] = (authorCount[author] || 0) + 1
  })
  let topAuthor = '无'
  let maxCount = 0
  for (const [author, count] of Object.entries(authorCount)) {
    if (count > maxCount) {
      maxCount = count
      topAuthor = `${author} (${count}篇)`
    }
  }
  return topAuthor
})

const filteredPosts = computed(() => {
  return posts.value.filter(post => {
    return searchText.value === '' || 
           post.title.toLowerCase().includes(searchText.value.toLowerCase()) ||
           (post.content && post.content.toLowerCase().includes(searchText.value.toLowerCase()))
  })
})

const fetchPosts = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/forum/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    posts.value = response.data
  } catch (error) {
    console.error('获取帖子列表失败', error)
  }
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  fetchPosts()
})
</script>

<style scoped>
.page-container { padding: var(--spacing-lg); }

.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: var(--spacing-lg);
}

.btn-back {
  padding: 10px 20px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  cursor: pointer;
  font-size: var(--font-size-base);
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all var(--transition-fast);
}

.btn-back:hover {
  background: var(--bg-tertiary);
  border-color: var(--primary-color);
}

.btn-icon { width: 16px; height: 16px; }

.page-header h2 {
  margin: 0;
  color: var(--text-primary);
  font-size: var(--h2-font-size);
  font-weight: var(--h2-font-weight);
  display: flex;
  align-items: center;
}

.header-icon { width: 28px; height: 28px; color: var(--primary-color); margin-right: 10px; }

.stats-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.summary-card {
  background: var(--bg-primary);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  text-align: center;
  transition: box-shadow var(--transition-normal);
}

.summary-card:hover { box-shadow: var(--shadow-md); }

.summary-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto var(--spacing-sm);
  background: rgba(13, 148, 136, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-svg { width: 24px; height: 24px; color: var(--primary-color); }

.summary-value {
  font-size: 32px;
  font-weight: var(--font-weight-bold);
  color: var(--primary-color);
  margin-bottom: 8px;
}

.summary-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.post-section h3 {
  margin-bottom: var(--spacing-md);
  color: var(--text-primary);
  font-size: var(--h4-font-size);
  font-weight: var(--h4-font-weight);
}

.filter-bar {
  margin-bottom: var(--spacing-md);
}

.search-input {
  width: 100%;
  max-width: 400px;
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-base);
  background: var(--bg-primary);
  transition: border-color var(--transition-fast);
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.post-card {
  background: var(--bg-primary);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  transition: box-shadow var(--transition-normal);
}

.post-card:hover { box-shadow: var(--shadow-md); }

.post-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.post-meta {
  display: flex;
  gap: var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-bottom: var(--spacing-sm);
}

.post-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.meta-icon-svg { width: 14px; height: 14px; }

.post-content {
  font-size: var(--font-size-base);
  color: var(--text-secondary);
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>