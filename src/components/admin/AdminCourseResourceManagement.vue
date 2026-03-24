<template>
  <div class="page-container">
    <div class="page-header">
      <h2>资源管理</h2>
      <div class="header-actions">
        <input v-model="searchText" placeholder="搜索资源名称..." class="search-input" />
        <select v-model="filterStatus" class="filter-select">
          <option value="">全部状态</option>
          <option value="active">已发布</option>
          <option value="pending">待审核</option>
          <option value="rejected">已拒绝</option>
        </select>
        <button @click="fetchResources" class="btn-refresh">刷新</button>
      </div>
    </div>

    <div class="table-card">
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>资源名称</th>
            <th>类型</th>
            <th>上传者</th>
            <th>所需积分</th>
            <th>下载次数</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="resource in filteredResources" :key="resource.id">
            <td class="id-cell">{{ resource.id }}</td>
            <td class="title-cell">{{ resource.title }}</td>
            <td><span class="type-tag">{{ resource.type?.name || resource.type || '未分类' }}</span></td>
            <td>{{ resource.uploader?.name || resource.uploader?.username || resource.teacher?.name || resource.teacher?.username || '-' }}</td>
            <td>{{ resource.points_required }}</td>
            <td>{{ resource.downloads }}</td>
            <td>
              <span :class="['status-badge', resource.status]">
                {{ statusText(resource.status) }}
              </span>
            </td>
            <td>
              <div class="actions">
                <button @click="viewResource(resource)" class="btn-view">查看</button>
                <button
                  v-if="resource.status === 'pending'"
                  @click="approveResource(resource)"
                  class="btn-approve">通过</button>
                <button
                  v-if="resource.status === 'active'"
                  @click="toggleStatus(resource)"
                  class="btn-disable">禁用</button>
                <button
                  v-if="resource.status === 'rejected'"
                  @click="toggleStatus(resource)"
                  class="btn-enable">启用</button>
                <button @click="deleteResource(resource.id)" class="btn-delete">删除</button>
              </div>
            </td>
          </tr>
          <tr v-if="filteredResources.length === 0">
            <td colspan="8" class="empty-row">暂无数据</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 查看详情弹窗 -->
    <div v-if="showDetailDialog" class="dialog-overlay" @click="showDetailDialog = false">
      <div class="dialog" @click.stop>
        <div class="dialog-header">
          <h3>资源详情</h3>
          <button @click="showDetailDialog = false" class="dialog-close">✕</button>
        </div>
        <div class="detail-body">
          <div class="detail-item"><span class="detail-label">名称</span><span>{{ detailResource.title }}</span></div>
          <div class="detail-item"><span class="detail-label">类型</span><span>{{ detailResource.type?.name || '-' }}</span></div>
          <div class="detail-item"><span class="detail-label">描述</span><span>{{ detailResource.description || '暂无' }}</span></div>
          <div class="detail-item"><span class="detail-label">文件地址</span>
            <a v-if="detailResource.file_url" :href="detailResource.file_url" target="_blank" class="file-link">点击访问</a>
            <span v-else>-</span>
          </div>
          <div class="detail-item"><span class="detail-label">所需积分</span><span>{{ detailResource.points_required }}</span></div>
          <div class="detail-item"><span class="detail-label">下载次数</span><span>{{ detailResource.downloads }}</span></div>
          <div class="detail-item" v-if="detailResource.reject_reason">
            <span class="detail-label">拒绝原因</span><span class="reject-reason">{{ detailResource.reject_reason }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const resources = ref<any[]>([])
const searchText = ref('')
const filterStatus = ref('')
const showDetailDialog = ref(false)
const detailResource = ref<any>({})

const filteredResources = computed(() => {
  return resources.value.filter(r => {
    const matchSearch = r.title?.toLowerCase().includes(searchText.value.toLowerCase())
    const matchStatus = !filterStatus.value || r.status === filterStatus.value
    return matchSearch && matchStatus
  })
})

const statusText = (s: string) => {
  const map: any = { active: '已发布', pending: '待审核', rejected: '已拒绝', approved: '已通过' }
  return map[s] || s
}

const fetchResources = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('http://127.0.0.1:8000/api/courses/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    // 管理员同时获取 pending 资源
    const pendingRes = await axios.get('http://127.0.0.1:8000/api/courses/pending/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    const all = [...res.data, ...pendingRes.data]
    // 去重
    const seen = new Set()
    resources.value = all.filter(r => {
      if (seen.has(r.id)) return false
      seen.add(r.id)
      return true
    })
  } catch (e) {
    console.error('获取资源列表失败', e)
  }
}

const viewResource = (resource: any) => {
  detailResource.value = resource
  showDetailDialog.value = true
}

const approveResource = async (resource: any) => {
  try {
    const token = localStorage.getItem('token')
    await axios.put(`http://127.0.0.1:8000/api/courses/${resource.id}/approve/`,
      { action: 'approve' },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    resource.status = 'active'
  } catch (e) {
    alert('操作失败')
  }
}

const toggleStatus = async (resource: any) => {
  try {
    const token = localStorage.getItem('token')
    const action = resource.status === 'active' ? 'reject' : 'approve'
    await axios.put(`http://127.0.0.1:8000/api/courses/${resource.id}/approve/`,
      { action },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    resource.status = action === 'approve' ? 'active' : 'rejected'
  } catch (e) {
    alert('操作失败')
  }
}

const deleteResource = async (id: number) => {
  if (confirm('确定要删除这个资源吗？')) {
    try {
      const token = localStorage.getItem('token')
      await axios.delete(`http://127.0.0.1:8000/api/courses/${id}/delete/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      resources.value = resources.value.filter(r => r.id !== id)
    } catch (e) {
      alert('删除失败')
    }
  }
}

onMounted(fetchResources)
</script>

<style scoped>
.page-container { padding: 24px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.page-header h2 { margin: 0; font-size: 22px; color: #1a1a2e; }
.header-actions { display: flex; gap: 12px; align-items: center; }
.search-input {
  padding: 9px 16px; border: 1px solid #dcdfe6; border-radius: 8px;
  font-size: 14px; width: 200px; outline: none;
}
.search-input:focus { border-color: #409eff; }
.filter-select {
  padding: 9px 14px; border: 1px solid #dcdfe6; border-radius: 8px;
  font-size: 14px; outline: none; background: white;
}
.btn-refresh {
  padding: 9px 18px; background: #f0f7ff; color: #409eff;
  border: 1px solid #c6e2ff; border-radius: 8px; cursor: pointer; font-size: 14px;
}
.btn-refresh:hover { background: #e0f0ff; }

.table-card { background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); overflow: hidden; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th {
  padding: 14px 16px; background: #f8f9fc; text-align: left;
  font-size: 13px; color: #606266; font-weight: 600; border-bottom: 1px solid #ebeef5;
}
.data-table td {
  padding: 13px 16px; font-size: 14px; color: #303133;
  border-bottom: 1px solid #f5f7fa;
}
.data-table tbody tr:hover { background: #fafbff; }
.data-table tbody tr:last-child td { border-bottom: none; }
.id-cell { color: #909399; font-size: 13px; }
.title-cell { font-weight: 500; max-width: 200px; }

.type-tag {
  display: inline-block; padding: 3px 10px;
  background: #ecf5ff; color: #409eff; border-radius: 20px; font-size: 12px;
}
.status-badge {
  display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 500;
}
.status-badge.active { background: #f0f9eb; color: #67c23a; }
.status-badge.pending { background: #fdf6ec; color: #e6a23c; }
.status-badge.rejected { background: #fef0f0; color: #f56c6c; }
.status-badge.approved { background: #f0f9eb; color: #67c23a; }

.empty-row { text-align: center; color: #c0c4cc; padding: 40px; }
.actions { display: flex; gap: 6px; flex-wrap: wrap; }
.btn-view, .btn-approve, .btn-disable, .btn-enable, .btn-delete {
  padding: 5px 12px; border: none; border-radius: 6px;
  cursor: pointer; font-size: 12px; font-weight: 500; transition: opacity 0.2s;
}
.btn-view { background: #f4f4f5; color: #606266; }
.btn-approve { background: #f0f9eb; color: #67c23a; }
.btn-disable { background: #fdf6ec; color: #e6a23c; }
.btn-enable { background: #ecf5ff; color: #409eff; }
.btn-delete { background: #fef0f0; color: #f56c6c; }
.btn-view:hover { background: #e9e9eb; }

.dialog-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.45); display: flex;
  justify-content: center; align-items: center; z-index: 1000;
}
.dialog {
  background: white; border-radius: 16px; width: 480px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}
.dialog-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 20px 24px 16px; border-bottom: 1px solid #f0f2f5;
}
.dialog-header h3 { margin: 0; font-size: 17px; color: #1a1a2e; }
.dialog-close {
  background: none; border: none; font-size: 18px;
  color: #909399; cursor: pointer; padding: 4px; border-radius: 4px;
}
.dialog-close:hover { background: #f5f5f5; }
.detail-body { padding: 20px 24px 24px; display: flex; flex-direction: column; gap: 14px; }
.detail-item { display: flex; gap: 16px; }
.detail-label { min-width: 72px; color: #909399; font-size: 13px; flex-shrink: 0; padding-top: 1px; }
.file-link { color: #409eff; text-decoration: none; }
.file-link:hover { text-decoration: underline; }
.reject-reason { color: #f56c6c; }
</style>