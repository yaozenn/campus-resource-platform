<template>
  <div class="page-container">
    <h2>公告管理</h2>
    <div class="toolbar">
      <button @click="showAddDialog = true" class="btn-add">发布公告</button>
      <button @click="fetchAnnouncements" class="btn-refresh">刷新</button>
    </div>
    <table class="data-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>标题</th>
          <th>发布者</th>
          <th>可见范围</th>
          <th>发布时间</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ann in announcements" :key="ann.id">
          <td>{{ ann.id }}</td>
          <td>{{ ann.title }}</td>
          <td>{{ ann.author?.username }}</td>
          <td><span class="visible-tag">{{ getVisibleText(ann.visible_to) }}</span></td>
          <td>{{ ann.publish_date }}</td>
          <td class="actions">
            <button @click="editAnnouncement(ann)" class="btn-edit">编辑</button>
            <button @click="deleteAnnouncement(ann.id)" class="btn-delete">删除</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="showAddDialog || showEditDialog" class="dialog-overlay" @click="closeDialog">
      <div class="dialog" @click.stop>
        <h3>{{ showEditDialog ? '编辑公告' : '发布公告' }}</h3>
        <form @submit.prevent="saveAnnouncement">
          <input v-model="currentAnnouncement.title" placeholder="标题" required />
          <textarea v-model="currentAnnouncement.content" placeholder="内容" rows="5" required></textarea>
          <select v-model="currentAnnouncement.visible_to">
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

const announcements = ref<any[]>([])
const showAddDialog = ref(false)
const showEditDialog = ref(false)
const currentAnnouncement = ref({ title: '', content: '', visible_to: 'all' })

const getVisibleText = (visible: string) => {
  const map: any = { all: '公开', student: '学生', teacher: '老师' }
  return map[visible] || visible
}

const fetchAnnouncements = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/announcements/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    announcements.value = response.data
  } catch (error) {
    console.error('获取公告列表失败', error)
  }
}

const editAnnouncement = (ann: any) => {
  currentAnnouncement.value = { ...ann }
  showEditDialog.value = true
}

const closeDialog = () => {
  showAddDialog.value = false
  showEditDialog.value = false
  currentAnnouncement.value = { title: '', content: '', visible_to: 'all' }
}

const saveAnnouncement = async () => {
  try {
    const token = localStorage.getItem('token')
    if (showEditDialog.value) {
      await axios.put(`http://127.0.0.1:8000/api/announcements/${currentAnnouncement.value.id}/`, currentAnnouncement.value, {
        headers: { Authorization: `Bearer ${token}` }
      })
    } else {
      await axios.post('http://127.0.0.1:8000/api/announcements/create/', currentAnnouncement.value, {
        headers: { Authorization: `Bearer ${token}` }
      })
    }
    closeDialog()
    fetchAnnouncements()
    alert('保存成功')
  } catch (error) {
    alert('保存失败')
  }
}

const deleteAnnouncement = async (id: number) => {
  if (confirm('确定要删除这个公告吗？')) {
    try {
      const token = localStorage.getItem('token')
      await axios.delete(`http://127.0.0.1:8000/api/announcements/${id}/delete/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      announcements.value = announcements.value.filter(a => a.id !== id)
      alert('删除成功')
    } catch (error) {
      alert('删除失败')
    }
  }
}

onMounted(() => {
  fetchAnnouncements()
})
</script>

<style scoped>
.page-container { padding: 20px; }
.toolbar { margin-bottom: 20px; display: flex; gap: 10px; }
.btn-add, .btn-refresh { padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; }
.btn-add { background: #67c23a; color: white; }
.btn-refresh { background: #409eff; color: white; }
.data-table { width: 100%; background: white; border-collapse: collapse; border-radius: 8px; overflow: hidden; }
.data-table th, .data-table td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }
.data-table th { background: #f5f7fa; font-weight: bold; }
.visible-tag { display: inline-block; padding: 2px 8px; background: #e6f7ff; color: #1890ff; border-radius: 4px; font-size: 12px; }
.actions { display: flex; gap: 5px; }
.btn-edit, .btn-delete { padding: 4px 10px; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; }
.btn-edit { background: #409eff; color: white; }
.btn-delete { background: #f56c6c; color: white; }
.dialog-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.dialog { background: white; padding: 24px; border-radius: 8px; min-width: 450px; }
.dialog h3 { margin: 0 0 16px; }
.dialog form { display: flex; flex-direction: column; gap: 12px; }
.dialog input, .dialog textarea, .dialog select { padding: 8px 12px; border: 1px solid #ddd; border-radius: 4px; }
.dialog-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 16px; }
.btn-cancel { padding: 8px 16px; border: 1px solid #ddd; background: white; border-radius: 4px; cursor: pointer; }
.btn-submit { padding: 8px 16px; background: #409eff; color: white; border: none; border-radius: 4px; cursor: pointer; }
</style>
