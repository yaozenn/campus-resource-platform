<template>
  <div class="page-container">
    <h2>论坛</h2>
    <div class="toolbar">
      <button @click="showPostDialog = true" class="btn-add">发帖</button>
    </div>
    <div class="post-list">
      <div v-for="post in posts" :key="post.id" class="post-item">
        <h3>{{ post.title }}</h3>
        <p>{{ post.content }}</p>
        <div class="post-info">
          <span>作者: {{ post.author?.name || post.author?.username }}</span>
          <span>时间: {{ post.post_date }}</span>
          <span class="visible-tag">{{ getVisibleText(post.visible_to) }}</span>
        </div>
      </div>
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
import { ref, onMounted } from 'vue'

import { useToast } from '../../composables/useToast'
import axios from 'axios'

  const toast = useToast()
const posts = ref<any[]>([])
const showPostDialog = ref(false)
const newPost = ref({ title: '', content: '', visible_to: 'all' })

const getVisibleText = (visible: string) => {
  const map: any = { all: '公开', student: '学生', teacher: '老师' }
  return map[visible] || visible
}

const fetchPosts = async () => {
  try {
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    const response = await axios.get(`http://127.0.0.1:8000/api/forum/?role=${user.role}`)
    posts.value = response.data
  } catch (error) {
    console.error('获取帖子失败', error)
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

onMounted(() => {
  fetchPosts()
})
</script>

<style scoped>
.page-container { padding: 20px; }
.toolbar { margin-bottom: 20px; }
.btn-add { padding: 8px 16px; background: #409eff; color: white; border: none; border-radius: 4px; cursor: pointer; }
.post-list { display: flex; flex-direction: column; gap: 15px; }
.post-item { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.post-item h3 { margin: 0 0 10px; }
.post-info { display: flex; justify-content: space-between; color: #999; font-size: 14px; margin-top: 10px; }
.visible-tag { background: #e6f7ff; color: #1890ff; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.dialog-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.dialog { background: white; padding: 24px; border-radius: 8px; min-width: 400px; }
.dialog h3 { margin: 0 0 16px; }
.dialog form { display: flex; flex-direction: column; gap: 12px; }
.dialog input, .dialog textarea, .dialog select { padding: 8px 12px; border: 1px solid #ddd; border-radius: 4px; }
.dialog-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 16px; }
.btn-cancel { padding: 8px 16px; border: 1px solid #ddd; background: white; border-radius: 4px; cursor: pointer; }
.btn-submit { padding: 8px 16px; background: #409eff; color: white; border: none; border-radius: 4px; cursor: pointer; }
</style>
