<template>
  <div class="page-container">
    <div class="page-header">
      <h2>积分管理</h2>
    </div>

    <el-tabs v-model="activeTab" @tab-change="onTabChange" class="points-tabs">
      <!-- 用户积分 -->
      <el-tab-pane label="用户积分" name="users">
        <div class="tab-toolbar">
          <input v-model="userSearch" placeholder="搜索用户名/姓名..." class="search-input" />
          <button @click="fetchUsers" class="btn-refresh">刷新</button>
        </div>
        <div class="table-card">
          <table class="data-table">
            <thead>
              <tr>
                <th>用户名</th><th>姓名</th><th>角色</th><th>积分</th><th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in filteredUsers" :key="user.id">
                <td>{{ user.username }}</td>
                <td>{{ user.name || '-' }}</td>
                <td><span :class="['role-badge', user.role]">{{ roleText(user.role) }}</span></td>
                <td><span class="points-cell">{{ user.points }} 分</span></td>
                <td>
                  <button @click="openAdjust(user)" class="btn-adjust">调整积分</button>
                </td>
              </tr>
              <tr v-if="filteredUsers.length === 0">
                <td colspan="5" class="empty-row">暂无数据</td>
              </tr>
            </tbody>
          </table>
        </div>
      </el-tab-pane>

      <!-- 奖品管理 -->
      <el-tab-pane label="奖品管理" name="prizes">
        <div class="tab-toolbar">
          <button @click="showAddPrizeDialog = true" class="btn-add">+ 添加奖品</button>
          <button @click="fetchPrizes" class="btn-refresh">刷新</button>
        </div>
        <div class="table-card">
          <table class="data-table">
            <thead>
              <tr>
                <th>奖品名称</th><th>描述</th><th>所需积分</th><th>库存</th><th>状态</th><th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="prize in prizes" :key="prize.id">
                <td class="prize-name">{{ prize.name }}</td>
                <td class="desc-cell">{{ prize.description || '-' }}</td>
                <td><span class="points-cell">{{ prize.points_required }} 分</span></td>
                <td>{{ prize.stock }}</td>
                <td>
                  <span :class="['status-badge', prize.is_active ? 'active' : 'inactive']">
                    {{ prize.is_active ? '上架' : '下架' }}
                  </span>
                </td>
                <td>
                  <div class="actions">
                    <button @click="editPrize(prize)" class="btn-edit">编辑</button>
                    <button @click="togglePrize(prize)" class="btn-toggle">
                      {{ prize.is_active ? '下架' : '上架' }}
                    </button>
                    <button @click="deletePrize(prize.id)" class="btn-delete">删除</button>
                  </div>
                </td>
              </tr>
              <tr v-if="prizes.length === 0">
                <td colspan="6" class="empty-row">暂无奖品</td>
              </tr>
            </tbody>
          </table>
        </div>
      </el-tab-pane>

      <!-- 兑换记录 -->
      <el-tab-pane label="兑换记录" name="exchanges">
        <div class="tab-toolbar">
          <button @click="fetchExchanges" class="btn-refresh">刷新</button>
        </div>
        <div class="table-card">
          <table class="data-table">
            <thead>
              <tr>
                <th>用户</th><th>奖品</th><th>消耗积分</th><th>状态</th><th>兑换时间</th><th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="ex in exchanges" :key="ex.id">
                <td>{{ ex.user?.username }}</td>
                <td>{{ ex.prize?.name }}</td>
                <td><span class="points-cell">{{ ex.points_spent }} 分</span></td>
                <td>
                  <span :class="['status-badge', ex.status]">{{ exchangeStatusText(ex.status) }}</span>
                </td>
                <td class="time-cell">{{ formatDate(ex.exchange_date) }}</td>
                <td>
                  <div class="actions" v-if="ex.status === 'pending'">
                    <button @click="approveExchange(ex)" class="btn-approve">通过</button>
                    <button @click="rejectExchange(ex)" class="btn-delete">拒绝</button>
                  </div>
                  <span v-else class="handled-text">已处理</span>
                </td>
              </tr>
              <tr v-if="exchanges.length === 0">
                <td colspan="6" class="empty-row">暂无记录</td>
              </tr>
            </tbody>
          </table>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 调整积分弹窗 -->
    <div v-if="showAdjustDialog" class="dialog-overlay" @click="showAdjustDialog = false">
      <div class="dialog" @click.stop>
        <div class="dialog-header">
          <h3>调整积分</h3>
          <button @click="showAdjustDialog = false" class="dialog-close">✕</button>
        </div>
        <div class="dialog-body">
          <div class="adjust-user-info">
            <span class="adjust-username">{{ currentUser?.username }}</span>
            <span class="adjust-current">当前积分：<b>{{ currentUser?.points }}</b></span>
          </div>
          <div class="form-group">
            <label>操作类型</label>
            <div class="type-toggle">
              <button :class="['toggle-btn', adjustType === 'add' ? 'active-add' : '']" @click="adjustType = 'add'">+ 增加积分</button>
              <button :class="['toggle-btn', adjustType === 'deduct' ? 'active-deduct' : '']" @click="adjustType = 'deduct'">- 扣除积分</button>
            </div>
          </div>
          <div class="form-group">
            <label>积分数量</label>
            <input v-model.number="adjustAmount" type="number" min="1" placeholder="请输入数量" class="form-input" />
          </div>
          <div class="form-group">
            <label>调整原因</label>
            <input v-model="adjustReason" placeholder="请输入原因" class="form-input" />
          </div>
        </div>
        <div class="dialog-footer">
          <button @click="showAdjustDialog = false" class="btn-cancel">取消</button>
          <button @click="submitAdjust" class="btn-submit">确认</button>
        </div>
      </div>
    </div>

    <!-- 添加/编辑奖品弹窗 -->
    <div v-if="showAddPrizeDialog || showEditPrizeDialog" class="dialog-overlay" @click="closePrizeDialog">
      <div class="dialog" @click.stop>
        <div class="dialog-header">
          <h3>{{ showEditPrizeDialog ? '编辑奖品' : '添加奖品' }}</h3>
          <button @click="closePrizeDialog" class="dialog-close">✕</button>
        </div>
        <div class="dialog-body">
          <div class="form-group">
            <label>奖品名称 <span class="required">*</span></label>
            <input v-model="currentPrize.name" placeholder="请输入奖品名称" class="form-input" required />
          </div>
          <div class="form-group">
            <label>奖品描述</label>
            <textarea v-model="currentPrize.description" placeholder="请输入描述" rows="3" class="form-input"></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>所需积分 <span class="required">*</span></label>
              <input v-model.number="currentPrize.points_required" type="number" min="0" class="form-input" />
            </div>
            <div class="form-group">
              <label>库存数量 <span class="required">*</span></label>
              <input v-model.number="currentPrize.stock" type="number" min="0" class="form-input" />
            </div>
          </div>
          <div class="form-group">
            <label>图片链接</label>
            <input v-model="currentPrize.image" placeholder="可选，填入图片URL" class="form-input" />
          </div>
        </div>
        <div class="dialog-footer">
          <button @click="closePrizeDialog" class="btn-cancel">取消</button>
          <button @click="savePrize" class="btn-submit">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const activeTab = ref('users')
const users = ref<any[]>([])
const prizes = ref<any[]>([])
const exchanges = ref<any[]>([])
const userSearch = ref('')

const showAdjustDialog = ref(false)
const currentUser = ref<any>(null)
const adjustType = ref<'add' | 'deduct'>('add')
const adjustAmount = ref(0)
const adjustReason = ref('')

const showAddPrizeDialog = ref(false)
const showEditPrizeDialog = ref(false)
const currentPrize = ref({ name: '', description: '', points_required: 0, stock: 0, image: '', is_active: true })

const filteredUsers = computed(() => {
  const q = userSearch.value.toLowerCase()
  if (!q) return users.value
  return users.value.filter(u => u.username?.toLowerCase().includes(q) || u.name?.toLowerCase().includes(q))
})

const roleText = (r: string) => ({ admin: '管理员', student: '学生', teacher: '老师' }[r] || r)
const exchangeStatusText = (s: string) => ({ pending: '待处理', approved: '已通过', rejected: '已拒绝' }[s] || s)
const formatDate = (d: string) => d ? new Date(d).toLocaleString('zh-CN') : '-'

const getToken = () => localStorage.getItem('token')
const headers = () => ({ Authorization: `Bearer ${getToken()}` })

const fetchUsers = async () => {
  try {
    const [t, s] = await Promise.all([
      axios.get('http://127.0.0.1:8000/api/auth/teachers/', { headers: headers() }),
      axios.get('http://127.0.0.1:8000/api/auth/students/', { headers: headers() })
    ])
    users.value = [...t.data, ...s.data]
  } catch (e) { console.error(e) }
}

const fetchPrizes = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/points/manage/', { headers: headers() })
    prizes.value = res.data
  } catch (e) { console.error(e) }
}

const fetchExchanges = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/points/all-exchanges/', { headers: headers() })
    exchanges.value = res.data
  } catch (e) { console.error(e) }
}

const onTabChange = (tab: string) => {
  if (tab === 'users' && users.value.length === 0) fetchUsers()
  if (tab === 'prizes' && prizes.value.length === 0) fetchPrizes()
  if (tab === 'exchanges' && exchanges.value.length === 0) fetchExchanges()
}

const openAdjust = (user: any) => {
  currentUser.value = { ...user }
  adjustType.value = 'add'
  adjustAmount.value = 0
  adjustReason.value = ''
  showAdjustDialog.value = true
}

const submitAdjust = async () => {
  if (!adjustAmount.value || adjustAmount.value <= 0) return alert('请输入有效积分数量')
  if (!adjustReason.value.trim()) return alert('请填写调整原因')
  try {
    const delta = adjustType.value === 'add' ? adjustAmount.value : -adjustAmount.value
    const newPoints = currentUser.value.points + delta
    // 使用管理员更新接口，直接修改目标用户积分
    await axios.put(
      `http://127.0.0.1:8000/api/auth/update/${currentUser.value.id}/`,
      { points: newPoints },
      { headers: headers() }
    )
    // 同步更新列表
    const target = users.value.find(u => u.id === currentUser.value.id)
    if (target) target.points = newPoints
    showAdjustDialog.value = false
    alert(`积分${adjustType.value === 'add' ? '增加' : '扣除'}成功`)
  } catch (e) {
    alert('操作失败')
  }
}

const editPrize = (prize: any) => {
  currentPrize.value = { ...prize }
  showEditPrizeDialog.value = true
}

const closePrizeDialog = () => {
  showAddPrizeDialog.value = false
  showEditPrizeDialog.value = false
  currentPrize.value = { name: '', description: '', points_required: 0, stock: 0, image: '', is_active: true }
}

const savePrize = async () => {
  try {
    if (showEditPrizeDialog.value) {
      await axios.put(`http://127.0.0.1:8000/api/points/manage/${(currentPrize.value as any).id}/`, currentPrize.value, { headers: headers() })
    } else {
      await axios.post('http://127.0.0.1:8000/api/points/manage/', currentPrize.value, { headers: headers() })
    }
    closePrizeDialog()
    fetchPrizes()
    alert('保存成功')
  } catch (e) { alert('保存失败') }
}

const togglePrize = async (prize: any) => {
  try {
    await axios.put(`http://127.0.0.1:8000/api/points/manage/${prize.id}/`, { ...prize, is_active: !prize.is_active }, { headers: headers() })
    prize.is_active = !prize.is_active
  } catch (e) { alert('操作失败') }
}

const deletePrize = async (id: number) => {
  if (confirm('确定删除？')) {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/points/delete/${id}/`, { headers: headers() })
      prizes.value = prizes.value.filter(p => p.id !== id)
    } catch (e) { alert('删除失败') }
  }
}

const approveExchange = async (ex: any) => {
  try {
    await axios.put(`http://127.0.0.1:8000/api/points/approve/${ex.id}/`, { action: 'approve' }, { headers: headers() })
    ex.status = 'approved'
  } catch (e) { alert('操作失败') }
}

const rejectExchange = async (ex: any) => {
  try {
    await axios.put(`http://127.0.0.1:8000/api/points/approve/${ex.id}/`, { action: 'reject' }, { headers: headers() })
    ex.status = 'rejected'
  } catch (e) { alert('操作失败') }
}

onMounted(fetchUsers)
</script>

<style scoped>
.page-container { padding: 24px; }
.page-header { margin-bottom: 20px; }
.page-header h2 { margin: 0; font-size: 22px; color: #1a1a2e; }

.tab-toolbar { display: flex; gap: 12px; align-items: center; margin: 16px 0; }
.search-input {
  padding: 9px 16px; border: 1px solid #dcdfe6; border-radius: 8px;
  font-size: 14px; width: 220px; outline: none;
}
.search-input:focus { border-color: #409eff; }
.btn-add {
  padding: 9px 18px; background: linear-gradient(135deg, #67c23a, #85ce61);
  color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 14px;
}
.btn-refresh {
  padding: 9px 18px; background: #f0f7ff; color: #409eff;
  border: 1px solid #c6e2ff; border-radius: 8px; cursor: pointer; font-size: 14px;
}

.table-card { background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); overflow: hidden; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th {
  padding: 14px 16px; background: #f8f9fc; text-align: left;
  font-size: 13px; color: #606266; font-weight: 600; border-bottom: 1px solid #ebeef5;
}
.data-table td { padding: 13px 16px; font-size: 14px; color: #303133; border-bottom: 1px solid #f5f7fa; }
.data-table tbody tr:hover { background: #fafbff; }
.data-table tbody tr:last-child td { border-bottom: none; }
.empty-row { text-align: center; color: #c0c4cc; padding: 40px; }
.desc-cell { color: #909399; font-size: 13px; max-width: 180px; }
.time-cell { color: #909399; font-size: 13px; }
.prize-name { font-weight: 500; }
.handled-text { color: #c0c4cc; font-size: 13px; }

.role-badge {
  display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight: 500;
}
.role-badge.admin { background: #fef0f0; color: #f56c6c; }
.role-badge.student { background: #ecf5ff; color: #409eff; }
.role-badge.teacher { background: #f0f9eb; color: #67c23a; }

.points-cell { font-weight: 600; color: #e6a23c; }

.status-badge {
  display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 500;
}
.status-badge.active, .status-badge.approved { background: #f0f9eb; color: #67c23a; }
.status-badge.inactive, .status-badge.rejected { background: #fef0f0; color: #f56c6c; }
.status-badge.pending { background: #fdf6ec; color: #e6a23c; }

.actions { display: flex; gap: 6px; }
.btn-adjust, .btn-edit, .btn-toggle, .btn-approve, .btn-delete {
  padding: 5px 12px; border: none; border-radius: 6px;
  cursor: pointer; font-size: 12px; font-weight: 500;
}
.btn-adjust { background: #ecf5ff; color: #409eff; }
.btn-edit { background: #ecf5ff; color: #409eff; }
.btn-toggle { background: #fdf6ec; color: #e6a23c; }
.btn-approve { background: #f0f9eb; color: #67c23a; }
.btn-delete { background: #fef0f0; color: #f56c6c; }

/* 弹窗 */
.dialog-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.45); display: flex;
  justify-content: center; align-items: center; z-index: 1000;
}
.dialog { background: white; border-radius: 16px; width: 480px; box-shadow: 0 20px 60px rgba(0,0,0,0.2); }
.dialog-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 20px 24px 16px; border-bottom: 1px solid #f0f2f5;
}
.dialog-header h3 { margin: 0; font-size: 17px; color: #1a1a2e; }
.dialog-close { background: none; border: none; font-size: 18px; color: #909399; cursor: pointer; }
.dialog-body { padding: 20px 24px; display: flex; flex-direction: column; gap: 16px; }
.dialog-footer {
  display: flex; justify-content: flex-end; gap: 12px;
  padding: 16px 24px 20px; border-top: 1px solid #f0f2f5;
}
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 13px; font-weight: 600; color: #606266; }
.required { color: #f56c6c; }
.form-input {
  padding: 9px 12px; border: 1px solid #dcdfe6; border-radius: 8px;
  font-size: 14px; outline: none; transition: border-color 0.2s;
}
.form-input:focus { border-color: #409eff; }
textarea.form-input { resize: vertical; }

.adjust-user-info {
  background: #f8f9fc; border-radius: 10px; padding: 14px 16px;
  display: flex; justify-content: space-between; align-items: center;
}
.adjust-username { font-weight: 600; color: #303133; }
.adjust-current { color: #909399; font-size: 13px; }
.adjust-current b { color: #e6a23c; font-size: 16px; }

.type-toggle { display: flex; gap: 0; border-radius: 8px; overflow: hidden; border: 1px solid #dcdfe6; }
.toggle-btn {
  flex: 1; padding: 9px; border: none; cursor: pointer; font-size: 14px;
  background: white; color: #606266; transition: all 0.2s;
}
.toggle-btn.active-add { background: #f0f9eb; color: #67c23a; font-weight: 600; }
.toggle-btn.active-deduct { background: #fef0f0; color: #f56c6c; font-weight: 600; }

.btn-cancel {
  padding: 9px 24px; border: 1px solid #dcdfe6; background: white;
  border-radius: 8px; cursor: pointer; font-size: 14px; color: #606266;
}
.btn-submit {
  padding: 9px 24px; background: linear-gradient(135deg, #409eff, #66b1ff);
  color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 500;
}
</style>