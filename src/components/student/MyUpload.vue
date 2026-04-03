<template>
  <div class="page-container fade-in">
    <div class="page-header">
      <div class="header-content">
        <h2>我的分享</h2>
        <p class="subtitle">上传课件、笔记或闲置书籍，赚取积分并帮助他人</p>
      </div>
      <button @click="openUploadModal" class="btn btn-primary">
        <IconUpload class="btn-icon" /> 发布新资源
      </button>
    </div>

    <div class="resource-grid">
      <div v-for="res in myResources" :key="res.id" class="resource-card card">
        <div class="card-status" :class="res.status">
          {{ getStatusText(res.status) }}
        </div>
        <div class="card-body">
          <h3 class="res-title">{{ res.title }}</h3>
          <p class="res-type">{{ res.type_name }}</p>
          <div class="res-meta">
            <span>下载: {{ res.downloads }} 次</span>
            <span v-if="res.is_second_hand" class="second-hand-tag">二手 ¥{{ res.price }}</span>
          </div>
          <p v-if="res.status === 'rejected'" class="reject-reason">
            驳回原因: {{ res.reject_reason || '不符合平台规范' }}
          </p>
        </div>
        <div class="card-footer">
          <button @click="deleteResource(res.id)" class="btn btn-danger btn-sm">删除</button>
        </div>
      </div>
      
      <div v-if="myResources.length === 0" class="empty-state card full-width">
        <p>你还没有分享过任何资源哦，快去发布一个吧！</p>
      </div>
    </div>

    <div v-if="showUploadModal" class="modal-overlay" @click="closeUploadModal">
      <div class="modal-card slide-up" @click.stop>
        <div class="modal-header">
          <h3>发布新资源</h3>
          <button @click="closeUploadModal" class="btn-close"><IconClose /></button>
        </div>
        <form @submit.prevent="submitResource" class="modal-body">
          
          <div class="form-group">
            <label>资源标题 <span class="required">*</span></label>
            <input v-model="formData.title" placeholder="如：2023年高等数学期末复习笔记" required class="input" />
          </div>

          <div class="form-group">
            <label>所属分类 <span class="required">*</span></label>
            <select v-model="formData.type_id" required class="input">
              <option value="" disabled>请选择分类</option>
              <optgroup v-for="(subTypes, mainCat) in groupedTypes" :key="mainCat" :label="String(mainCat)">
                <option v-for="t in subTypes" :key="t.id" :value="t.id">{{ t.name }}</option>
              </optgroup>
            </select>
          </div>

          <div class="form-group">
            <label>资源描述</label>
            <textarea v-model="formData.description" placeholder="简要介绍这份资料的内容和适用人群..." rows="3" class="input"></textarea>
          </div>

          <div class="form-group">
            <label>文件或网盘链接 <span class="required">*</span></label>
            <input v-model="formData.file_url" placeholder="请填写百度网盘链接或其他文件地址" required class="input" />
          </div>

          <div class="form-row">
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.is_second_hand" />
              这是闲置二手实体书/物品
            </label>
          </div>
          <div v-if="formData.is_second_hand" class="form-group">
            <label>转让价格 (¥)</label>
            <input v-model="formData.price" type="number" step="0.01" min="0" placeholder="例如：15.5" class="input" />
          </div>

          <div class="modal-footer">
            <button type="button" @click="closeUploadModal" class="btn btn-secondary">取消</button>
            <button type="submit" class="btn btn-primary">提交审核</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { IconUpload, IconClose } from '../icons'

const myResources = ref<any[]>([])
const types = ref<any[]>([])
const showUploadModal = ref(false)

const formData = ref({
  title: '', type_id: '', description: '', file_url: '', 
  points_required: 0, is_second_hand: false, price: 0
})

const groupedTypes = computed(() => {
  const groups: Record<string, any[]> = {}
  types.value.forEach(t => {
    const main = t.description || '其他未分类'
    if (!groups[main]) groups[main] = []
    groups[main].push(t)
  })
  return groups
})

const getStatusText = (status: string) => ({ pending: '待审核', active: '已发布', rejected: '已驳回' }[status] || '未知')

const fetchMyResources = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('http://127.0.0.1:8000/api/courses/teacher/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    myResources.value = res.data
  } catch (error) {
    console.error('获取列表失败', error)
  }
}

const fetchTypes = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/courses/types/')
    types.value = res.data
  } catch (error) { console.error('获取分类失败') }
}

const openUploadModal = () => { showUploadModal.value = true }
const closeUploadModal = () => {
  showUploadModal.value = false
  formData.value = { title: '', type_id: '', description: '', file_url: '', points_required: 0, is_second_hand: false, price: 0 }
}

const submitResource = async () => {
  if (!formData.value.type_id) {
    alert('请选择资源分类！')
    return
  }

  try {
    const token = localStorage.getItem('token')
    if (!formData.value.is_second_hand) formData.value.price = 0
    
    const payload = {
      ...formData.value,
      type_id: Number(formData.value.type_id),
      price: Number(formData.value.price || 0),
      points_required: Number(formData.value.points_required || 0)
    }
    
    await axios.post('http://127.0.0.1:8000/api/courses/create/', payload, {
      headers: { Authorization: `Bearer ${token}` }
    })
    alert('提交成功，请等待管理员审核！')
    closeUploadModal()
    fetchMyResources()
  } catch (error: any) { 
    console.error('上传失败详情:', error.response?.data)
    const errorMsg = error.response?.data?.type_id?.[0] || 
                     error.response?.data?.file_url?.[0] || 
                     error.response?.data?.detail ||
                     '提交失败，请检查填写内容'
    alert(errorMsg)
  }
}

const deleteResource = async (id: number) => {
  if (!confirm('确定要删除这份资源吗？')) return
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`http://127.0.0.1:8000/api/courses/${id}/delete/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    alert('删除成功')
    fetchMyResources()
  } catch (error) { alert('删除失败') }
}

onMounted(() => {
  fetchMyResources()
  fetchTypes()
})
</script>

<style scoped>
/* 此处保留你原本的所有样式，完全不动 */
.page-container { padding: var(--spacing-lg); max-width: 1200px; margin: 0 auto; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--spacing-xl); }
.page-header h2 { font-size: var(--font-size-2xl); font-weight: 600; color: var(--text-primary); margin-bottom: var(--spacing-xs); font-family: var(--font-sf); }
.subtitle { color: var(--text-secondary); font-size: var(--font-size-sm); }
.btn { display: flex; align-items: center; gap: 8px; padding: 10px 20px; border-radius: var(--border-radius-md); font-weight: 500; font-size: 14px; cursor: pointer; border: none; transition: all 0.2s; }
.btn-primary { background: var(--primary-color); color: white; }
.btn-primary:hover { background: var(--primary-dark); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(13, 148, 136, 0.2); }
.btn-secondary { background: var(--bg-tertiary); color: var(--text-secondary); }
.btn-danger { background: rgba(239, 68, 68, 0.1); color: #ef4444; }
.btn-danger:hover { background: #ef4444; color: white; }
.btn-sm { padding: 6px 14px; font-size: 13px; }
.resource-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
.card { background: var(--bg-primary); border-radius: var(--border-radius-lg); border: 1px solid var(--border-light); position: relative; overflow: hidden; display: flex; flex-direction: column; }
.card-status { position: absolute; top: 12px; right: 12px; font-size: 12px; padding: 4px 10px; border-radius: 12px; font-weight: 600; }
.card-status.pending { background: #fef3c7; color: #d97706; }
.card-status.active { background: #d1fae5; color: #059669; }
.card-status.rejected { background: #fee2e2; color: #dc2626; }
.card-body { padding: 20px; flex: 1; margin-top: 10px;}
.res-title { font-size: 16px; font-weight: 600; color: var(--text-primary); margin: 0 0 8px; }
.res-type { font-size: 13px; color: var(--text-secondary); margin-bottom: 12px; }
.res-meta { display: flex; gap: 12px; font-size: 13px; color: var(--text-tertiary); }
.second-hand-tag { color: #f59e0b; font-weight: 600; }
.reject-reason { font-size: 12px; color: #dc2626; background: #fee2e2; padding: 8px; border-radius: 4px; margin-top: 12px; }
.card-footer { padding: 12px 20px; border-top: 1px solid var(--border-light); display: flex; justify-content: flex-end; }
.full-width { grid-column: 1 / -1; }
.empty-state { padding: 60px; text-align: center; color: var(--text-tertiary); }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 2000; }
.modal-card { background: var(--bg-primary); width: 100%; max-width: 500px; border-radius: var(--border-radius-xl); box-shadow: var(--shadow-xl); overflow: hidden; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 1px solid var(--border-light); background: var(--bg-secondary); }
.modal-header h3 { margin: 0; font-size: 18px; font-weight: 600; }
.btn-close { background: none; border: none; cursor: pointer; color: var(--text-tertiary); display: flex; }
.modal-body { padding: 24px; display: flex; flex-direction: column; gap: 16px; }
.form-group { display: flex; flex-direction: column; gap: 8px; }
.form-group label { font-size: 14px; font-weight: 500; color: var(--text-secondary); }
.required { color: #ef4444; }
.input { padding: 10px 14px; border: 1px solid var(--border-color); border-radius: var(--border-radius-md); background: var(--bg-secondary); color: var(--text-primary); transition: all 0.2s; font-size: 14px;}
.input:focus { border-color: var(--primary-color); outline: none; background: var(--bg-primary); }
.form-row { display: flex; align-items: center; }
.checkbox-label { display: flex; align-items: center; gap: 8px; font-size: 14px; color: var(--text-primary); cursor: pointer; }
.modal-footer { margin-top: 10px; display: flex; justify-content: flex-end; gap: 12px; }
.fade-in { animation: fadeIn var(--transition-normal); }
.slide-up { animation: slideUp var(--transition-normal); }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>