<template>
  <div class="page-container">
    <div class="page-header">
      <h2>老师管理</h2>
      <div class="header-actions">
        <input v-model="searchText" placeholder="搜索姓名/用户名..." class="search-input" />
        <button @click="showAddDialog = true" class="btn-add">+ 添加老师</button>
      </div>
    </div>

    <div class="table-card">
      <table class="data-table">
        <thead>
          <tr>
            <th>工号</th>
            <th>用户名</th>
            <th>姓名</th>
            <th>性别</th>
            <th>手机号</th>
            <th>学科</th>
            <th>部门</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="teacher in filteredTeachers" :key="teacher.id">
            <td>{{ teacher.employee_id || '-' }}</td>
            <td>{{ teacher.username }}</td>
            <td>{{ teacher.name || '-' }}</td>
            <td>{{ getGenderText(teacher.gender) }}</td>
            <td>{{ teacher.phone || '-' }}</td>
            <td>{{ teacher.subject || '-' }}</td>
            <td>{{ teacher.department || '-' }}</td>
            <td>
              <div class="actions">
                <button @click="editTeacher(teacher)" class="btn-edit">编辑</button>
                <button @click="deleteTeacher(teacher.id)" class="btn-delete">删除</button>
              </div>
            </td>
          </tr>
          <tr v-if="filteredTeachers.length === 0">
            <td colspan="8" class="empty-row">暂无数据</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showAddDialog || showEditDialog" class="dialog-overlay" @click="closeDialog">
      <div class="dialog" @click.stop>
        <div class="dialog-header">
          <h3>{{ showEditDialog ? '编辑老师' : '添加老师' }}</h3>
          <button @click="closeDialog" class="dialog-close">✕</button>
        </div>
        <form @submit.prevent="saveTeacher" class="dialog-form">
          <div class="form-row">
            <div class="form-group" v-if="showAddDialog">
              <label>用户名 <span class="required">*</span></label>
              <input v-model="currentTeacher.username" placeholder="请输入用户名" required />
            </div>
            <div class="form-group" v-if="showAddDialog">
              <label>密码 <span class="required">*</span></label>
              <input v-model="currentTeacher.password" type="password" placeholder="请输入密码" required />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>姓名</label>
              <input v-model="currentTeacher.name" placeholder="请输入姓名" />
            </div>
            <div class="form-group">
              <label>工号</label>
              <input v-model="currentTeacher.employee_id" placeholder="请输入工号" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>性别</label>
              <select v-model="currentTeacher.gender">
                <option value="">请选择</option>
                <option value="male">男</option>
                <option value="female">女</option>
                <option value="other">其他</option>
              </select>
            </div>
            <div class="form-group">
              <label>手机号</label>
              <input v-model="currentTeacher.phone" placeholder="请输入手机号" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>学科</label>
              <input v-model="currentTeacher.subject" placeholder="请输入学科" />
            </div>
            <div class="form-group">
              <label>部门</label>
              <input v-model="currentTeacher.department" placeholder="请输入部门" />
            </div>
          </div>
          <div class="form-group">
            <label>个性签名</label>
            <input v-model="currentTeacher.signature" placeholder="请输入个性签名" />
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
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const teachers = ref<any[]>([])
const searchText = ref('')
const showAddDialog = ref(false)
const showEditDialog = ref(false)
const currentTeacher = ref({
  username: '', password: '', employee_id: '', name: '',
  gender: '', phone: '', signature: '', subject: '', department: ''
})

const filteredTeachers = computed(() => {
  const q = searchText.value.toLowerCase()
  if (!q) return teachers.value
  return teachers.value.filter(t =>
    t.username?.toLowerCase().includes(q) || t.name?.toLowerCase().includes(q)
  )
})

const getGenderText = (gender: string) => {
  const map: any = { male: '男', female: '女', other: '其他' }
  return map[gender] || '-'
}

const fetchTeachers = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('http://127.0.0.1:8000/api/auth/teachers/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    teachers.value = res.data
  } catch (e) {
    console.error('获取老师列表失败', e)
  }
}

const editTeacher = (teacher: any) => {
  currentTeacher.value = { ...teacher, password: '' }
  showEditDialog.value = true
}

const closeDialog = () => {
  showAddDialog.value = false
  showEditDialog.value = false
  currentTeacher.value = {
    username: '', password: '', employee_id: '', name: '',
    gender: '', phone: '', signature: '', subject: '', department: ''
  }
}

const saveTeacher = async () => {
  try {
    const token = localStorage.getItem('token')
    if (showEditDialog.value) {
      const { password, ...updateData } = currentTeacher.value
      await axios.put(`http://127.0.0.1:8000/api/auth/update/${(currentTeacher.value as any).id}/`, updateData, {
        headers: { Authorization: `Bearer ${token}` }
      })
    } else {
      await axios.post('http://127.0.0.1:8000/api/auth/create/', {
        ...currentTeacher.value, role: 'teacher'
      }, { headers: { Authorization: `Bearer ${token}` } })
    }
    closeDialog()
    fetchTeachers()
    alert('保存成功')
  } catch (e) {
    alert('保存失败')
  }
}

const deleteTeacher = async (id: number) => {
  if (confirm('确定要删除这个老师吗？')) {
    try {
      const token = localStorage.getItem('token')
      await axios.delete(`http://127.0.0.1:8000/api/auth/delete/${id}/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      teachers.value = teachers.value.filter(t => t.id !== id)
      alert('删除成功')
    } catch (e) {
      alert('删除失败')
    }
  }
}

onMounted(fetchTeachers)
</script>

<style scoped>
.page-container { padding: 24px; }

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.page-header h2 { margin: 0; font-size: 22px; color: #1a1a2e; }
.header-actions { display: flex; gap: 12px; align-items: center; }
.search-input {
  padding: 9px 16px;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  font-size: 14px;
  width: 220px;
  outline: none;
  transition: border-color 0.2s;
}
.search-input:focus { border-color: #409eff; }
.btn-add {
  padding: 9px 20px;
  background: linear-gradient(135deg, #67c23a, #85ce61);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
}
.btn-add:hover { opacity: 0.88; }

.table-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  overflow: hidden;
}
.data-table { width: 100%; border-collapse: collapse; }
.data-table th {
  padding: 14px 16px;
  background: #f8f9fc;
  text-align: left;
  font-size: 13px;
  color: #606266;
  font-weight: 600;
  border-bottom: 1px solid #ebeef5;
}
.data-table td {
  padding: 14px 16px;
  font-size: 14px;
  color: #303133;
  border-bottom: 1px solid #f5f7fa;
}
.data-table tbody tr:hover { background: #fafbff; }
.data-table tbody tr:last-child td { border-bottom: none; }

.empty-row { text-align: center; color: #c0c4cc; padding: 40px; }

.actions { display: flex; gap: 8px; }
.btn-edit, .btn-delete {
  padding: 5px 14px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: opacity 0.2s;
}
.btn-edit { background: #ecf5ff; color: #409eff; }
.btn-edit:hover { background: #d9ecff; }
.btn-delete { background: #fef0f0; color: #f56c6c; }
.btn-delete:hover { background: #fde2e2; }

.dialog-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.45);
  display: flex; justify-content: center; align-items: center;
  z-index: 1000;
}
.dialog {
  background: white;
  border-radius: 16px;
  width: 560px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}
.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px 16px;
  border-bottom: 1px solid #f0f2f5;
}
.dialog-header h3 { margin: 0; font-size: 17px; color: #1a1a2e; }
.dialog-close {
  background: none; border: none; font-size: 18px;
  color: #909399; cursor: pointer; padding: 4px;
  border-radius: 4px;
}
.dialog-close:hover { background: #f5f5f5; color: #303133; }

.dialog-form { padding: 20px 24px 24px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
.form-group { display: flex; flex-direction: column; gap: 6px; margin-bottom: 16px; }
.form-group label { font-size: 13px; font-weight: 600; color: #606266; }
.required { color: #f56c6c; }
.form-group input, .form-group select {
  padding: 9px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}
.form-group input:focus, .form-group select:focus {
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64,158,255,0.1);
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #f0f2f5;
}
.btn-cancel {
  padding: 9px 24px;
  border: 1px solid #dcdfe6;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #606266;
}
.btn-cancel:hover { background: #f5f5f5; }
.btn-submit {
  padding: 9px 24px;
  background: linear-gradient(135deg, #409eff, #66b1ff);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
}
.btn-submit:hover { opacity: 0.88; }
</style>
