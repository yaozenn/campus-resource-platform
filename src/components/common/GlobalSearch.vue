<template>
  <div class="global-search">
    <!-- 搜索按钮 -->
    <button class="search-trigger" @click="openSearch" :title="shortcutHint">
      <IconSearch class="search-icon" />
      <span class="search-hint">搜索</span>
      <kbd class="shortcut-kbd">Ctrl+K</kbd>
    </button>

    <!-- 搜索弹窗 -->
    <transition name="search-modal">
      <div v-if="isOpen" class="search-overlay" @click.self="closeSearch">
        <div class="search-modal">
          <!-- 搜索头部 -->
          <div class="search-header">
            <IconSearch class="search-input-icon" />
            <input
              ref="searchInput"
              v-model="searchQuery"
              placeholder="搜索资源、课程、论坛帖子..."
              class="search-input"
              @input="handleSearch"
              @keydown.esc="closeSearch"
              @keydown.down.prevent="navigateResults('down')"
              @keydown.up.prevent="navigateResults('up')"
              @keydown.enter="selectResult"
            />
            <button v-if="searchQuery" class="clear-btn" @click="clearSearch">
              <IconClose class="clear-icon" />
            </button>
          </div>

          <!-- 搜索历史 -->
          <div v-if="!searchQuery && searchHistory.length > 0" class="search-history">
            <div class="history-header">
              <IconClock class="history-icon" />
              <span>最近搜索</span>
              <button class="clear-history" @click="clearHistory">清除历史</button>
            </div>
            <div class="history-tags">
              <button
                v-for="(history, index) in searchHistory"
                :key="index"
                class="history-tag"
                @click="selectHistory(history)"
              >
                {{ history }}
              </button>
            </div>
          </div>

          <!-- 热门搜索 -->
          <div v-if="!searchQuery && !searchHistory.length" class="hot-search">
            <div class="hot-header">
              <IconFlame class="hot-icon" />
              <span>热门搜索</span>
            </div>
            <div class="hot-tags">
              <button
                v-for="(tag, index) in hotSearches"
                :key="index"
                class="hot-tag"
                @click="selectHotSearch(tag)"
              >
                {{ tag }}
              </button>
            </div>
          </div>

          <!-- 搜索结果 -->
          <div v-else-if="searchQuery" class="search-results">
            <div v-if="loading" class="search-loading">
              <LoadingSpinner size="32px" />
              <span>搜索中...</span>
            </div>
            <div v-else-if="results.length === 0" class="search-empty">
              <IconInbox class="empty-icon" />
              <p>未找到相关结果</p>
            </div>
            <div v-else class="results-list">
              <div
                v-for="(result, index) in results"
                :key="result.id"
                :class="['result-item', { active: selectedIndex === index }]"
                @click="selectResult(result)"
                @mouseenter="selectedIndex = index"
              >
                <div class="result-icon">
                  <IconBook v-if="result.type === 'resource'" class="result-icon-svg" />
                  <IconMessageCircle v-else-if="result.type === 'forum'" class="result-icon-svg" />
                  <IconVideo v-else-if="result.type === 'course'" class="result-icon-svg" />
                </div>
                <div class="result-content">
                  <div class="result-title" v-html="highlightText(result.title)"></div>
                  <div class="result-desc">{{ result.description }}</div>
                </div>
                <IconArrowRight class="result-arrow" />
              </div>
            </div>
          </div>

          <!-- 搜索底部提示 -->
          <div class="search-footer">
            <span class="footer-tip">
              <kbd>↑</kbd><kbd>↓</kbd> 导航
              <kbd>↵</kbd> 选择
              <kbd>ESC</kbd> 关闭
            </span>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import {
  IconSearch,
  IconClose,
  IconClock,
  IconFlame,
  IconInbox,
  IconArrowRight,
  IconBook,
  IconMessageCircle,
  IconVideo
} from '@/components/icons'
import LoadingSpinner from './LoadingSpinner.vue'
import axios from 'axios'

const router = useRouter()
const isOpen = ref(false)
const searchQuery = ref('')
const searchHistory = ref<string[]>([])
const hotSearches = ref<string[]>(['网络课程', '校内资源', '电子书', '论坛', '学习'])
const results = ref<any[]>([])
const loading = ref(false)
const selectedIndex = ref(-1)

const searchInput = ref<HTMLInputElement | null>(null)

const shortcutHint = computed(() => {
  const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0
  return isMac ? '⌘+K' : 'Ctrl+K'
})

// 键盘快捷键
const handleKeydown = (e: KeyboardEvent) => {
  const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault()
    isOpen.value ? closeSearch() : openSearch()
  }
}

// 打开搜索
const openSearch = async () => {
  isOpen.value = true
  await nextTick()
  searchInput.value?.focus()
  loadHistory()
}

// 关闭搜索
const closeSearch = () => {
  isOpen.value = false
  searchQuery.value = ''
  results.value = []
  selectedIndex.value = -1
}

// 加载搜索历史
const loadHistory = () => {
  const history = localStorage.getItem('search_history')
  if (history) {
    searchHistory.value = JSON.parse(history)
  }
}

// 保存搜索历史
const saveHistory = (query: string) => {
  if (!query.trim()) return
  
  // 移除重复项
  const index = searchHistory.value.indexOf(query)
  if (index !== -1) {
    searchHistory.value.splice(index, 1)
  }
  
  // 添加到开头
  searchHistory.value.unshift(query)
  
  // 限制历史记录数量
  if (searchHistory.value.length > 10) {
    searchHistory.value.pop()
  }
  
  localStorage.setItem('search_history', JSON.stringify(searchHistory.value))
}

// 清除历史
const clearHistory = () => {
  searchHistory.value = []
  localStorage.removeItem('search_history')
}

// 选择历史
const selectHistory = (query: string) => {
  searchQuery.value = query
  handleSearch()
}

// 选择热门搜索
const selectHotSearch = (query: string) => {
  searchQuery.value = query
  handleSearch()
}

// 执行搜索
const handleSearch = () => {
  if (!searchQuery.value.trim()) {
    results.value = []
    return
  }

  loading.value = true
  selectedIndex.value = -1

  // 防抖
  clearTimeout((handleSearch as any).timeout)
  ;(handleSearch as any).timeout = setTimeout(async () => {
    try {
      const token = localStorage.getItem('token')
      
      // 尝试调用后端 API，如果失败则使用模拟数据
      try {
        const [resourcesRes, forumRes] = await Promise.all([
          axios.get(`http://127.0.0.1:8000/api/resources/search/?q=${encodeURIComponent(searchQuery.value)}`, {
            headers: { Authorization: `Bearer ${token}` },
            timeout: 5000
          }),
          axios.get(`http://127.0.0.1:8000/api/forum/search/?q=${encodeURIComponent(searchQuery.value)}`, {
            headers: { Authorization: `Bearer ${token}` },
            timeout: 5000
          })
        ])

        results.value = [
          ...resourcesRes.data.map((r: any) => ({ ...r, type: 'resource' })),
          ...forumRes.data.map((f: any) => ({ ...f, type: 'forum' }))
        ].slice(0, 10)
      } catch (apiError) {
        // API 调用失败，使用模拟数据演示
        console.log('搜索 API 未就绪，使用演示数据')
        results.value = [
          { id: 1, title: '计算机网络课程', description: '计算机网络基础教程', type: 'resource' },
          { id: 2, title: '数据结构与算法', description: '数据结构入门课程', type: 'course' },
          { id: 3, title: '校园生活讨论', description: '关于校园生活的交流帖子', type: 'forum' },
          { id: 4, title: 'Python 编程资源', description: 'Python 学习资料集合', type: 'resource' },
          { id: 5, title: '图书馆使用指南', description: '图书馆资源使用说明', type: 'resource' }
        ].filter(item => 
          item.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          item.description.toLowerCase().includes(searchQuery.value.toLowerCase())
        ).slice(0, 10)
      }
    } catch (error) {
      console.error('搜索失败', error)
    } finally {
      loading.value = false
    }
  }, 300)
}

// 导航搜索结果
const navigateResults = (direction: 'up' | 'down') => {
  if (direction === 'down') {
    selectedIndex.value = Math.min(selectedIndex.value + 1, results.value.length - 1)
  } else {
    selectedIndex.value = Math.max(selectedIndex.value - 1, 0)
  }
}

// 选择结果
const selectResult = (result?: any) => {
  if (!result && selectedIndex.value >= 0) {
    result = results.value[selectedIndex.value]
  }
  
  if (!result) return

  // 保存搜索历史
  saveHistory(searchQuery.value)

  // 路由跳转
  if (result.type === 'resource') {
    router.push(`/student/courses?search=${result.id}`)
  } else if (result.type === 'forum') {
    router.push(`/student/forum/${result.id}`)
  } else if (result.type === 'course') {
    router.push(`/student/courses?id=${result.id}`)
  }

  closeSearch()
}

// 清除搜索
const clearSearch = () => {
  searchQuery.value = ''
  results.value = []
  searchInput.value?.focus()
}

// 高亮文本
const highlightText = (text: string) => {
  if (!searchQuery.value) return text
  const regex = new RegExp(`(${searchQuery.value})`, 'gi')
  return text.replace(regex, '<mark>$1</mark>')
}

// 生命周期
onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
/* 搜索触发按钮 */
.search-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
}

.search-trigger:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.search-icon {
  width: 16px;
  height: 16px;
}

.search-hint {
  font-size: 14px;
}

.shortcut-kbd {
  padding: 2px 6px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  font-size: 11px;
  font-family: monospace;
}

/* 搜索弹窗 */
.search-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 80px;
  z-index: 9999;
}

.search-modal {
  width: 100%;
  max-width: 560px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.search-header {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.search-input-icon {
  width: 20px;
  height: 20px;
  color: #909399;
  margin-right: 12px;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 16px;
  color: #303133;
}

.clear-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  color: #909399;
}

.clear-icon {
  width: 18px;
  height: 18px;
}

/* 搜索历史 */
.search-history {
  padding: 16px 20px;
}

.history-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 14px;
  color: #909399;
}

.history-icon {
  width: 16px;
  height: 16px;
}

.clear-history {
  margin-left: auto;
  background: none;
  border: none;
  color: #909399;
  cursor: pointer;
  font-size: 12px;
}

.clear-history:hover {
  color: #409eff;
}

.history-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.history-tag {
  padding: 6px 12px;
  background: #f5f7fa;
  border: none;
  border-radius: 16px;
  color: #606266;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.3s;
}

.history-tag:hover {
  background: #e4e7ed;
  color: #409eff;
}

/* 热门搜索 */
.hot-search {
  padding: 16px 20px;
}

.hot-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 14px;
  color: #909399;
}

.hot-icon {
  width: 16px;
  height: 16px;
  color: #f59e0b;
}

.hot-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.hot-tag {
  padding: 6px 12px;
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  border: none;
  border-radius: 16px;
  color: #92400e;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.3s;
}

.hot-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

/* 搜索结果 */
.search-results {
  max-height: 400px;
  overflow-y: auto;
}

.search-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 40px;
  color: #909399;
}

.search-empty {
  text-align: center;
  padding: 40px;
  color: #909399;
}

.empty-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 12px;
}

.results-list {
  padding: 8px 0;
}

.result-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.result-item:hover,
.result-item.active {
  background: #f5f7fa;
}

.result-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.result-icon-svg {
  width: 20px;
  height: 20px;
  color: #409eff;
}

.result-content {
  flex: 1;
  min-width: 0;
}

.result-title {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.result-title :deep(mark) {
  background: #fef3c7;
  color: #92400e;
  padding: 0 2px;
  border-radius: 2px;
}

.result-desc {
  font-size: 12px;
  color: #909399;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.result-arrow {
  width: 18px;
  height: 18px;
  color: #c0c4cc;
  opacity: 0;
  transition: opacity 0.3s;
}

.result-item:hover .result-arrow,
.result-item.active .result-arrow {
  opacity: 1;
}

/* 搜索底部 */
.search-footer {
  padding: 12px 20px;
  border-top: 1px solid #f0f0f0;
  background: #fafafa;
}

.footer-tip {
  font-size: 12px;
  color: #909399;
  display: flex;
  gap: 8px;
}

.footer-tip kbd {
  padding: 2px 6px;
  background: #f5f7fa;
  border-radius: 4px;
  font-family: monospace;
  border: 1px solid #e4e7ed;
}

/* 过渡动画 */
.search-modal-enter-active,
.search-modal-leave-active {
  transition: all 0.3s ease;
}

.search-modal-enter-from {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

.search-modal-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}
</style>
