<template>
  <div class="page-container">
    <h2>类型管理</h2>
    <div class="toolbar">
      <button @click="showAddDialog = true" class="btn-add">添加类型</button>
    </div>
    
    <div class="type-list">
      <div v-for="type in types" :key="type.id" class="type-item">
        <div class="type-info">
          <h3>{{ type.name }}</h3>
          <p>{{ type.description || '无描述' }}</p>
          <span class="create-time">{{ formatDate(type.created_at) }}</span>
        </div>
        <div class="type-actions">
          <button @click="editType(type)" class="btn-edit">编辑</button>
          <button @click="deleteType(type.id)" class="btn-delete">删除</button>
        </div>
      </div>
    </div>
    
    <div v-if="types.length === 0" class="empty-state">
      <p>暂无课程类型</p>
    </div>

    <!-- 添加/编辑对话框 -->
    <div v-if="showAddDialog || showEditDialog" class="dialog-overlay" @click="closeDialog">
      <div class="dialog" @click.stop>
        <h3>{{ showEditDialog ? '编辑类型' : '添加类型' }}</h3>
        <form @submit.prevent="saveType">
          <div class="form-group">
            <label>类型名称</label>
            <input v-model="formData.name" placeholder="请输入类型名称" required />
          </div>
          <div class="form-group">
            <label>类型描述</label>
            <textarea v-model="formData.description" placeholder="请输入类型描述" rows="3"></textarea>
          </div>
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

const types = ref<any[]>([])
const showAddDialog = ref(false)
const showEditDialog = ref(false)
const formData = ref({ name: '', description: '' })
const editingType = ref<number | null>(null)

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

const fetchTypes = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/courses/types/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    types.value = response.data
  } catch (error) {
    console.error('获取课程类型失败', error)
  }
}

const saveType = async () => {
  try {
    const token = localStorage.getItem('token')
    const url = editingType.value 
      ? `http://127.0.0.1:8000/api/courses/types/${editingType.value}/` 
      : 'http://127.0.0.1:8000/api/courses/types/'
    
    const method = editingType.value ? 'put' : 'post'
    await axios[method](url, formData.value, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    closeDialog()
    fetchTypes()
    alert('保存成功')
  } catch (error) {
    alert('保存失败')
  }
}

const editType = (type: any) => {
  formData.value = { ...type }
  editingType.value = type.id
  showEditDialog.value = true
  showAddDialog.value = false
}

const deleteType = async (id: number) => {
  if (confirm('确定要删除这个类型吗？')) {
    try {
      const token = localStorage.getItem('token')
      await axios.delete(`http://127.0.0.1:8000/api/courses/types/${id}/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      fetchTypes()
      alert('删除成功')
    } catch (error) {
      alert('删除失败')
    }
  }
}

const closeDialog = () => {
  showAddDialog.value = false
  showEditDialog.value = false
  formData.value = { name: '', description: '' }
  editingType.value = null
}

onMounted(() => {
  fetchTypes()
})
</script>

<style scoped>
.page-container { padding: 20px; }
.toolbar { margin-bottom: 20px; }
.btn-add { padding: 8px 16px; background: #409eff; color: white; border: none; border-radius: 4px; cursor: pointer; }
.type-list { display: flex; flex-direction: column; gap: 15px; }
.type-item { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: flex-start; }
.type-info { flex: 1; }
.type-info h3 { margin: 0 0 8px; color: #333; }
.type-info p { margin: 0 0 8px; color: #666; }
.create-time { font-size: 12px; color: #999; }
.type-actions { display: flex; gap: 10px; }
.btn-edit { padding: 6px 12px; background: #52c41a; color: white; border: none; border-radius: 4px; cursor: pointer; }
.btn-delete { padding: 6px 12px; background: #ff4d4f; color: white; border: none; border-radius: 4px; cursor: pointer; }
.empty-state { text-align: center; padding: 60px 20px; color: #999; }
.dialog-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.dialog { background: white; padding: 24px; border-radius: 8px; min-width: 400px; }
.dialog h3 { margin: 0 0 16px; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; margin-bottom: 8px; color: #666; font-weight: 500; }
.form-group input, .form-group textarea { width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
.dialog-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; }
.btn-cancel { padding: 8px 16px; border: 1px solid #ddd; background: white; border-radius: 4px; cursor: pointer; }
.btn-submit { padding: 8px 16px; background: #409eff; color: white; border: none; border-radius: 4px; cursor: pointer; }
</style>
