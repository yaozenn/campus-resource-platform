<template>
  <div class="page-container">
    <div class="forum-header">
      <h2>
        <IconMessageCircle class="header-icon" />
        交流论坛
      </h2>
      <button @click="showPostDialog = true" class="btn-add">
        <IconEdit class="btn-icon-svg" />
        <span>发布帖子</span>
      </button>
    </div>
    
    <div class="search-bar">
      <IconSearch class="search-icon" />
      <input
        v-model="searchText"
        placeholder="搜索帖子..."
        class="search-input"
      />
      <button v-if="searchText" @click="searchText = ''" class="clear-btn">
        <IconClose class="clear-icon" />
      </button>
    </div>
    
    <div class="sort-bar">
      <div class="sort-label">
        <IconSort class="sort-icon" />
        <span>排序：</span>
      </div>
      <button 
        v-for="option in sortOptions" 
        :key="option.value"
        @click="sortBy = option.value"
        :class="['sort-btn', { active: sortBy === option.value }]"
      >
        {{ option.label }}
      </button>
    </div>
    
    <div class="post-list">
      <!-- 加载状态 -->
      <template v-if="loading">
        <div v-for="i in 5" :key="i" class="post-item skeleton">
          <div class="post-avatar">
            <div class="avatar-circle skeleton-avatar"></div>
          </div>
          <div class="post-content">
            <div class="skeleton-line title"></div>
            <div class="skeleton-line content"></div>
            <div class="skeleton-line footer"></div>
          </div>
        </div>
      </template>
      
      <!-- 帖子列表 -->
      <template v-else-if="filteredPosts.length > 0">
        <div v-for="post in filteredPosts" :key="post.id" class="post-item" @click="viewPost(post)">
          <div class="post-avatar">
            <Avatar 
              :avatar="post.author?.avatar" 
              :name="post.author?.name || post.author?.username || 'U'"
              :size="48"
            />
          </div>
          
          <div class="post-content">
            <div class="post-header">
              <h3 class="post-title">
                <span v-if="isHotPost(post)" class="hot-tag">
                  <IconFlame class="hot-icon" />
                  热门
                </span>
                {{ post.title }}
              </h3>
              <span class="visible-tag">{{ getVisibleText(post.visible_to) }}</span>
            </div>
            
            <p class="post-excerpt">{{ post.content.substring(0, 120) }}{{ post.content.length > 120 ? '...' : '' }}</p>
            
            <div class="post-footer">
              <div class="post-author">
                <span class="author-name">{{ post.author?.name || post.author?.username }}</span>
                <span class="post-time">{{ formatTime(post.post_date) }}</span>
              </div>
              
              <div class="post-stats">
                <span class="stat-item" title="浏览量">
                  <IconEye class="stat-icon-svg" />
                  <span class="stat-value">{{ post.views || 0 }}</span>
                </span>
                <span class="stat-item" title="回复数">
                  <IconMessageCircle class="stat-icon-svg" />
                  <span class="stat-value">{{ post.replies || 0 }}</span>
                </span>
              </div>
            </div>
          </div>
        </div>
      </template>
      
      <!-- 空状态 -->
      <EmptyState
        v-else
        type="no-data"
        :title="searchText ? '未找到匹配的帖子' : '暂无帖子'"
        :description="searchText ? '尝试其他关键词' : '快来发布第一条帖子，开启交流之旅吧！'"
        :show-action="!searchText"
        action-text="发布帖子"
        @action="showPostDialog = true"
      />
    </div>

    <div v-if="showPostDialog" class="dialog-overlay" @click="showPostDialog = false">
      <div class="dialog" @click.stop>
        <h3>发布帖子</h3>
        <form @submit.prevent="createPost">
          <input v-model="newPost.title" placeholder="标题" required />
          <textarea v-model="newPost.content" placeholder="内容" rows="5" required></textarea>
          <select v-model="newPost.visible_to">
            <option value="all">公开</option>
            <option value="student">仅学生</option>
            <option value="teacher">仅老师</option>
          </select>
          <div class="dialog-actions">
            <button type="button" @click="showPostDialog = false" class="btn-cancel">取消</button>
            <button type="submit" class="btn-submit">发布</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import { formatTime } from '../../utils/timeFormat'
import { useRouter } from 'vue-router'
import { useToast } from '../../composables/useToast'
import { IconMessageCircle, IconEdit, IconFlame, IconEye, IconSearch, IconClose, IconSort } from '../../components/icons'
import EmptyState from '../common/EmptyState.vue'
import Avatar from '../common/Avatar.vue'

const toast = useToast()
const posts = ref<any[]>([])
const loading = ref(false)
const showPostDialog = ref(false)
const newPost = ref({ title: '', content: '', visible_to: 'all' })
const searchText = ref('')
const sortBy = ref('newest')
const sortOptions = [
  { label: '最新发布', value: 'newest' },
  { label: '最早发布', value: 'oldest' },
  { label: '热度最高', value: 'hot' }
]

const router = useRouter()

const isHotPost = (post: any) => {
  const views = post.views || 0
  const replies = post.replies || 0
  return views > 100 || replies > 20
}

const getVisibleText = (visible: string) => {
  const map: any = { all: '公开', student: '学生', teacher: '老师' }
  return map[visible] || visible
}

const filteredPosts = computed(() => {
  if (!searchText.value) {
    return posts.value
  }
  const search = searchText.value.toLowerCase()
  return posts.value.filter(post => 
    post.title.toLowerCase().includes(search) || 
    post.content.toLowerCase().includes(search)
  )
})

const viewPost = (post: any) => {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  if (user.role === 'teacher') {
    router.push(`/teacher/forum/${post.id}`)
  } else if (user.role === 'admin') {
    router.push(`/admin/forum/${post.id}`)
  } else {
    router.push(`/student/forum/${post.id}`)
  }
}

const fetchPosts = async () => {
  loading.value = true
  try {
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    const response = await axios.get(`http://127.0.0.1:8000/api/forum/?role=${user.role}&sort_by=${sortBy.value}`)
    posts.value = response.data
  } catch (error) {
    console.error('获取帖子失败', error)
  } finally {
    loading.value = false
  }
}

const createPost = async () => {
  try {
    const token = localStorage.getItem('token')
    await axios.post('http://127.0.0.1:8000/api/forum/create/', newPost.value, {
      headers: { Authorization: `Bearer ${token}` }
    })
    showPostDialog.value = false
    newPost.value = { title: '', content: '', visible_to: 'all' }
    fetchPosts()
    toast.success('发布成功')
  } catch (error) {
    toast.error('发布失败')
  }
}

watch(sortBy, () => {
  fetchPosts()
})

onMounted(() => {
  fetchPosts()
})
</script>

<style scoped>
.page-container { 
  padding: 24px; 
  background-color: var(--color-background);
  min-height: 100vh;
}

.forum-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 2px solid var(--border-color);
}

.forum-header h2 {
  margin: 0;
  color: var(--text-primary);
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  width: 28px;
  height: 28px;
  color: var(--primary-color);
}

.btn-add {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  color: white;
  border: none;
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  transition: all var(--transition-fast);
  box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3);
}

.btn-add:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(13, 148, 136, 0.4);
}

.btn-icon-svg {
  width: 18px;
  height: 18px;
}

.search-bar {
  position: relative;
  display: flex;
  align-items: center;
  margin-bottom: 24px;
  background: var(--bg-primary);
  border: 2px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  padding: 0 16px;
  transition: all 0.2s;
}
.search-bar:focus-within {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
}
.search-icon {
  width: 20px;
  height: 20px;
  color: var(--text-placeholder);
  flex-shrink: 0;
}
.search-input {
  flex: 1;
  padding: 14px 12px;
  border: none;
  background: transparent;
  font-size: 15px;
  outline: none;
  color: var(--text-primary);
}
.search-input::placeholder {
  color: var(--text-placeholder);
}
.sort-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  padding: 12px 16px;
  background: var(--bg-primary);
  border: 2px solid var(--border-color);
  border-radius: var(--border-radius-lg);
}

.sort-label {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

.sort-icon {
  width: 16px;
  height: 16px;
}

.sort-btn {
  padding: 6px 14px;
  border: 2px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: transparent;
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all 0.2s;
}

.sort-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.sort-btn.active {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.clear-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  background: var(--bg-secondary);
  border-radius: 50%;
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.2s;
}
.clear-btn:hover {
  background: var(--border-color);
}
.clear-icon {
  width: 16px;
  height: 16px;
  color: var(--text-secondary);
}

.post-list { 
  display: flex; 
  flex-direction: column; 
  gap: 16px; 
}

.post-item { 
  background: var(--bg-primary);
  padding: 24px; 
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-light);
  transition: all var(--transition-fast);
  cursor: pointer;
  display: flex;
  gap: 16px;
}

/* 骨架屏样式 */
.post-item.skeleton {
  pointer-events: none;
  animation: pulse 1.5s ease-in-out infinite;
}

.skeleton-avatar {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.skeleton-line {
  height: 16px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  border-radius: 4px;
  margin-bottom: 8px;
  animation: shimmer 1.5s infinite;
}

.skeleton-line.title {
  height: 20px;
  width: 70%;
  margin-bottom: 12px;
}

.skeleton-line.content {
  height: 16px;
  width: 100%;
  margin-bottom: 12px;
}

.skeleton-line.footer {
  height: 14px;
  width: 60%;
  margin-bottom: 0;
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}

.post-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-light);
}

.post-avatar {
  flex-shrink: 0;
}

.avatar-circle {
  width: 48px;
  height: 48px;
  border-radius: var(--border-radius-full);
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  box-shadow: var(--shadow-sm);
}

.post-content {
  flex: 1;
  min-width: 0;
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  gap: 12px;
}

.post-title {
  margin: 0;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  line-height: 1.4;
  display: flex;
  align-items: center;
  gap: 8px;
}

.hot-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
  color: white;
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  animation: pulse 2s ease-in-out infinite;
}

.hot-icon {
  width: 14px;
  height: 14px;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.visible-tag { 
  display: inline-block;
  padding: 4px 12px; 
  background: var(--primary-light); 
  color: var(--primary-color); 
  border-radius: var(--border-radius); 
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  white-space: nowrap;
}

.post-excerpt {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  line-height: 1.6;
  margin: 0 0 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid var(--border-light);
}

.post-author {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-name {
  color: var(--text-primary);
  font-weight: var(--font-weight-medium);
  font-size: var(--font-size-sm);
}

.post-time {
  color: var(--text-placeholder);
  font-size: var(--font-size-xs);
}

.post-stats {
  display: flex;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.stat-icon-svg {
  width: 16px;
  height: 16px;
  color: var(--text-tertiary);
}

.stat-value {
  font-weight: var(--font-weight-medium);
}

.empty-state { 
  text-align: center; 
  padding: 80px 20px; 
  color: var(--text-placeholder);
}

.empty-icon-svg {
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
  color: var(--text-tertiary);
}

/* 弹窗样式 */
.dialog-overlay { 
  position: fixed; 
  top: 0; 
  left: 0; 
  right: 0; 
  bottom: 0; 
  background: rgba(0, 0, 0, 0.5); 
  display: flex; 
  justify-content: center; 
  align-items: center; 
  z-index: 1000;
  animation: fadeIn var(--transition-fast);
}

.dialog { 
  background: var(--bg-primary);
  padding: 24px; 
  border-radius: var(--border-radius-lg); 
  min-width: 450px;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-color);
  animation: slideIn var(--transition-normal);
}

.dialog h3 { 
  margin: 0 0 20px; 
  color: var(--text-primary);
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
}

.dialog form { 
  display: flex; 
  flex-direction: column; 
  gap: 16px; 
}

.dialog input, 
.dialog textarea, 
.dialog select { 
  padding: 12px 16px; 
  border: 1px solid var(--border-color); 
  border-radius: var(--border-radius);
  font-size: var(--font-size-base);
  transition: all var(--transition-fast);
  background: var(--bg-primary);
  color: var(--text-primary);
}

.dialog input:focus,
.dialog textarea:focus,
.dialog select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
}

.dialog-actions { 
  display: flex; 
  justify-content: flex-end; 
  gap: 12px; 
  margin-top: 24px; 
}

.btn-cancel { 
  padding: 10px 20px; 
  border: 1px solid var(--border-color); 
  background: var(--bg-primary); 
  border-radius: var(--border-radius); 
  cursor: pointer;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  transition: all var(--transition-fast);
}

.btn-cancel:hover {
  background: var(--bg-secondary);
  border-color: var(--text-secondary);
}

.btn-submit { 
  padding: 10px 20px; 
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  color: white; 
  border: none; 
  border-radius: var(--border-radius); 
  cursor: pointer;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  transition: all var(--transition-fast);
  box-shadow: 0 2px 8px rgba(13, 148, 136, 0.3);
}

.btn-submit:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(13, 148, 136, 0.4);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .forum-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .forum-header h2 {
    font-size: var(--font-size-xl);
  }
  
  .btn-add {
    justify-content: center;
  }
  
  .post-item {
    flex-direction: column;
    padding: 16px;
  }
  
  .post-avatar {
    align-self: flex-start;
  }
  
  .post-footer {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
}
</style>