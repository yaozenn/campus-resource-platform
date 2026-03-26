<template>
  <div class="page-container">
    <h2>
      <IconMessageCircle class="header-icon" />
      论坛管理
    </h2>
    <div class="toolbar">
      <button @click="showAddDialog = true" class="btn-add">
        <IconPlus class="btn-icon-svg" />
        发布帖子
      </button>
      <button @click="fetchPosts" class="btn-refresh">
        <IconRefresh class="btn-icon-svg" />
        刷新
      </button>
    </div>
    <table class="data-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>标题</th>
          <th>作者</th>
          <th>可见范围</th>
          <th>发布时间</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="post in posts" :key="post.id">
          <td>{{ post.id }}</td>
          <td>{{ post.title }}</td>
          <td>{{ post.author?.username }}</td>
          <td><span class="visible-tag">{{ getVisibleText(post.visible_to) }}</span></td>
          <td>{{ post.post_date }}</td>
          <td class="actions">
            <button @click="editPost(post)" class="btn-edit">
              <IconEdit class="action-icon-svg" />
              编辑
            </button>
            <button @click="deletePost(post.id)" class="btn-delete">
              <IconDelete class="action-icon-svg" />
              删除
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="showAddDialog || showEditDialog" class="dialog-overlay" @click="closeDialog">
      <div class="dialog" @click.stop>
        <h3>{{ showEditDialog ? '编辑帖子' : '发布帖子' }}</h3>
        <form @submit.prevent="savePost">
          <input v-model="currentPost.title" placeholder="标题" required />
          <textarea v-model="currentPost.content" placeholder="内容" rows="5" required></textarea>
          <select v-model="currentPost.visible_to">
            <option value="all">公开</option>
            <option value="student">仅学生</option>
            <option value="teacher">仅老师</option>
          </select>
          <div class="dialog-actions">
            <button type="button" @click="closeDialog" class="btn-cancel">取消</button>
            <button type="submit" class="btn-submit">保存</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { IconMessageCircle, IconPlus, IconRefresh, IconEdit, IconDelete } from '@/components/icons'

const posts = ref<any[]>([])
const showAddDialog = ref(false)
const showEditDialog = ref(false)
const currentPost = ref({ title: '', content: '', visible_to: 'all' })

const getVisibleText = (visible: string) => {
  const map: any = { all: '公开', student: '学生', teacher: '老师' }
  return map[visible] || visible
}

const fetchPosts = async () => {
  try {
    const token = localStorage.getItem('token')
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    const response = await axios.get(`http://127.0.0.1:8000/api/forum/?role=${user.role}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    posts.value = response.data
  } catch (error) {
    console.error('获取帖子列表失败', error)
    alert('获取帖子列表失败，请检查网络连接')
  }
}

const editPost = (post: any) => {
  currentPost.value = { ...post }
  showEditDialog.value = true
}

const savePost = async () => {
  try {
    const token = localStorage.getItem('token')
    if (showEditDialog.value) {
      // 编辑现有帖子
      await axios.put(`http://127.0.0.1:8000/api/forum/${(currentPost.value as any).id}/`, currentPost.value, {
        headers: { Authorization: `Bearer ${token}` }
      })
    } else {
      // 发布新帖子
      await axios.post('http://127.0.0.1:8000/api/forum/create/', currentPost.value, {
        headers: { Authorization: `Bearer ${token}` }
      })
    }
    closeDialog()
    fetchPosts()
    alert('保存成功')
  } catch (error) {
    alert('保存失败')
  }
}

const closeDialog = () => {
  showAddDialog.value = false
  showEditDialog.value = false
  currentPost.value = { title: '', content: '', visible_to: 'all' }
}

const deletePost = async (id: number) => {
  if (confirm('确定要删除这个帖子吗？')) {
    try {
      const token = localStorage.getItem('token')
      await axios.delete(`http://127.0.0.1:8000/api/forum/${id}/delete/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      posts.value = posts.value.filter(p => p.id !== id)
      alert('删除成功')
    } catch (error) {
      alert('删除失败')
    }
  }
}

onMounted(() => {
  fetchPosts()
})
</script>

<style scoped>
.page-container { padding: var(--spacing-lg); }
.page-container h2 { margin: 0 0 var(--spacing-lg); font-size: var(--h2-font-size); font-weight: var(--h2-font-weight); color: var(--text-primary); display: flex; align-items: center; }
.header-icon { width: 28px; height: 28px; color: var(--primary-color); margin-right: 10px; }
.toolbar { margin-bottom: var(--spacing-lg); display: flex; gap: var(--spacing-md); }
.btn-add, .btn-refresh { padding: 10px 20px; border: none; border-radius: var(--border-radius-md); cursor: pointer; display: flex; align-items: center; gap: 8px; font-size: var(--font-size-base); font-weight: var(--font-weight-medium); transition: all var(--transition-normal); }
.btn-add { background: var(--primary-color); color: white; }
.btn-add:hover { background: var(--primary-hover); transform: translateY(-1px); box-shadow: var(--shadow-md); }
.btn-refresh { background: var(--bg-secondary); color: var(--text-primary); border: 1px solid var(--border-color); }
.btn-refresh:hover { background: var(--bg-tertiary); border-color: var(--primary-color); }
.btn-icon-svg { width: 16px; height: 16px; }
.data-table { width: 100%; background: var(--bg-primary); border-collapse: collapse; border-radius: var(--border-radius-lg); overflow: hidden; box-shadow: var(--shadow-sm); }
.data-table th, .data-table td { padding: 14px 16px; text-align: left; border-bottom: 1px solid var(--border-light); }
.data-table th { background: var(--bg-secondary); font-weight: var(--font-weight-semibold); color: var(--text-primary); font-size: var(--font-size-sm); }
.data-table tbody tr:hover { background: var(--bg-secondary); }
.visible-tag { display: inline-block; padding: 4px 12px; background: rgba(13, 148, 136, 0.1); color: var(--primary-color); border-radius: var(--border-radius-full); font-size: var(--font-size-xs); font-weight: var(--font-weight-medium); }
.actions { display: flex; gap: 8px; }
.btn-edit, .btn-delete { padding: 6px 12px; border: none; border-radius: var(--border-radius-md); cursor: pointer; font-size: var(--font-size-sm); display: flex; align-items: center; gap: 4px; transition: all var(--transition-fast); }
.action-icon-svg { width: 14px; height: 14px; }
.btn-edit { background: rgba(13, 148, 136, 0.1); color: var(--primary-color); }
.btn-edit:hover { background: var(--primary-color); color: white; }
.btn-delete { background: rgba(239, 68, 68, 0.1); color: var(--danger-color); }
.btn-delete:hover { background: var(--danger-color); color: white; }
.dialog-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.dialog { background: white; padding: 24px; border-radius: 8px; min-width: 450px; }
.dialog h3 { margin: 0 0 16px; }
.dialog form { display: flex; flex-direction: column; gap: 12px; }
.dialog input, .dialog textarea, .dialog select { padding: 8px 12px; border: 1px solid #ddd; border-radius: 4px; }
.dialog-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 16px; }
.btn-cancel { padding: 8px 16px; border: 1px solid #ddd; background: white; border-radius: 4px; cursor: pointer; }
.btn-submit { padding: 8px 16px; background: #409eff; color: white; border: none; border-radius: 4px; cursor: pointer; }
</style>
