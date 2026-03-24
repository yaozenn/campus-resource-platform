<template>
  <div class="page-container">
    <h2>资源管理</h2>
    <div class="toolbar">
      <button @click="showAddDialog = true" class="btn-add">添加资源</button>
      <button @click="fetchCourses" class="btn-refresh">刷新</button>
    </div>
    <table class="data-table">
      <thead>
        <tr>
          <th>资源名称</th>
          <th>类型</th>
          <th>所需积分</th>
          <th>是否二手</th>
          <th>价格</th>
          <th>下载次数</th>
          <th>状态</th>
          <th>上传时间</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="course in courses" :key="course.id">
          <td>{{ course.title }}</td>
          <td>{{ course.type?.name || '未分类' }}</td>
          <td>{{ course.points_required }}</td>
          <td>{{ course.is_second_hand ? '是' : '否' }}</td>
          <td>{{ course.price || '0' }}</td>
          <td>{{ course.downloads }}</td>
          <td><span :class="['status-tag', course.status]">{{ getStatusText(course.status) }}</span></td>
          <td>{{ course.upload_date }}</td>
          <td class="actions">
            <button @click="editCourse(course)" class="btn-edit">编辑</button>
            <button @click="deleteCourse(course.id)" class="btn-delete">删除</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 添加/编辑对话框 -->
    <div v-if="showAddDialog || showEditDialog" class="dialog-overlay" @click="closeDialog">
      <div class="dialog" @click.stop>
        <h3>{{ showEditDialog ? '编辑资源' : '添加资源' }}</h3>
        <form @submit.prevent="saveCourse">
          <div class="form-group">
            <label>资源名称</label>
            <input v-model="currentCourse.title" placeholder="请输入资源名称" required />
          </div>
          <div class="form-group">
            <label>资源类型</label>
            <select v-model="currentCourse.type" required>
              <option value="">请选择类型</option>
              <option v-for="type in courseTypes" :key="type.id" :value="type.id">
                {{ type.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>资源描述</label>
            <textarea v-model="currentCourse.description" placeholder="请输入资源描述" rows="3"></textarea>
          </div>
          <div class="form-group">
            <label>文件地址</label>
            <input v-model="currentCourse.file_url" placeholder="请输入文件地址" />
          </div>
          <div class="form-group">
            <label>所需积分</label>
            <input v-model.number="currentCourse.points_required" type="number" min="0" placeholder="请输入所需积分" />
          </div>
          <div class="form-group">
            <label>是否二手</label>
            <input v-model="currentCourse.is_second_hand" type="checkbox" />
          </div>
          <div class="form-group">
            <label>价格</label>
            <input v-model.number="currentCourse.price" type="number" min="0" step="0.01" placeholder="请输入价格" />
          </div>
          <div class="form-group">
            <label>封面图片</label>
            <input v-model="currentCourse.cover_image" placeholder="请输入封面图片地址" />
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

const courses = ref<any[]>([])
const courseTypes = ref<any[]>([])
const showAddDialog = ref(false)
const showEditDialog = ref(false)
const currentCourse = ref({
  id: 0,
  title: '',
  type: '',
  description: '',
  file_url: '',
  points_required: 0,
  is_second_hand: false,
  price: 0,
  cover_image: ''
})

const getStatusText = (status: string) => {
  const map: any = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝',
    active: '已发布'
  }
  return map[status] || status
}

const fetchCourses = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/courses/teacher/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    courses.value = response.data
  } catch (error) {
    console.error('获取资源列表失败', error)
  }
}

const fetchCourseTypes = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/courses/types/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    courseTypes.value = response.data
  } catch (error) {
    console.error('获取资源类型失败', error)
  }
}

const editCourse = (course: any) => {
  currentCourse.value = {
    id: course.id,
    title: course.title,
    type: course.type?.id || '',
    description: course.description || '',
    file_url: course.file_url || '',
    points_required: course.points_required || 0,
    is_second_hand: course.is_second_hand || false,
    price: course.price || 0,
    cover_image: course.cover_image || ''
  }
  showEditDialog.value = true
}

const closeDialog = () => {
  showAddDialog.value = false
  showEditDialog.value = false
  currentCourse.value = {
    id: 0,
    title: '',
    type: '',
    description: '',
    file_url: '',
    points_required: 0,
    is_second_hand: false,
    price: 0,
    cover_image: ''
  }
}

const saveCourse = async () => {
  try {
    const token = localStorage.getItem('token')
    if (showEditDialog.value) {
      // 编辑现有课程
      await axios.put(`http://127.0.0.1:8000/api/courses/${currentCourse.value.id}/`, currentCourse.value, {
        headers: { Authorization: `Bearer ${token}` }
      })
    } else {
      // 添加新课程
      await axios.post('http://127.0.0.1:8000/api/courses/create/', currentCourse.value, {
        headers: { Authorization: `Bearer ${token}` }
      })
    }
    closeDialog()
    fetchCourses()
    alert('保存成功')
  } catch (error) {
    alert('保存失败')
  }
}

const deleteCourse = async (id: number) => {
  if (confirm('确定要删除这个课程吗？')) {
    try {
      const token = localStorage.getItem('token')
      await axios.delete(`http://127.0.0.1:8000/api/courses/${id}/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      courses.value = courses.value.filter(c => c.id !== id)
      alert('删除成功')
    } catch (error) {
      alert('删除失败')
    }
  }
}

onMounted(() => {
  fetchCourses()
  fetchCourseTypes()
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
.status-tag { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.status-tag.pending { background: #fdf6ec; color: #e6a23c; }
.status-tag.approved, .status-tag.active { background: #f0f9eb; color: #67c23a; }
.status-tag.rejected { background: #fef0f0; color: #f56c6c; }
.actions { display: flex; gap: 5px; }
.btn-edit, .btn-delete { padding: 4px 10px; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; }
.btn-edit { background: #409eff; color: white; }
.btn-delete { background: #f56c6c; color: white; }
.dialog-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.dialog { background: white; padding: 24px; border-radius: 8px; min-width: 450px; max-height: 90vh; overflow-y: auto; }
.dialog h3 { margin: 0 0 16px; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; margin-bottom: 8px; color: #666; font-weight: 500; }
.form-group input, .form-group textarea, .form-group select { width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
.dialog-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; }
.btn-cancel { padding: 8px 16px; border: 1px solid #ddd; background: white; border-radius: 4px; cursor: pointer; }
.btn-submit { padding: 8px 16px; background: #409eff; color: white; border: none; border-radius: 4px; cursor: pointer; }
</style>
