  <template>
    <div class="page-container fade-in">
      <div class="page-header">
        <h2>我的积分与福利</h2>
        <p class="subtitle">完成平台任务赚取积分，免费兑换专属奖品</p>
      </div>

      <div class="points-overview-card card">
        <div class="overview-left">
          <div class="points-icon-wrapper">
            <IconStar class="huge-icon" />
          </div>
          <div class="points-text">
            <span class="label">当前可用积分</span>
            <h1 class="value">{{ userPoints }}</h1>
          </div>
        </div>
        <div class="overview-right">
          <button 
            @click="handleSign" 
            :class="['btn', hasSigned ? 'btn-secondary' : 'btn-primary btn-glow']"
            :disabled="hasSigned"
          >
            <IconCheck v-if="hasSigned" class="btn-icon" />
            <IconCalendar v-else class="btn-icon" />
            {{ hasSigned ? '今日已签到' : '立即签到领积分' }}
          </button>
        </div>
      </div>

      <div class="section-container">
        <h3 class="section-title">如何赚取更多积分？</h3>
        <div class="task-grid">
          <div class="task-card">
            <div class="task-icon bg-blue-soft"><IconUpload class="text-blue" /></div>
            <div class="task-info">
              <h4>分享优质资源</h4>
              <p>上传课件、笔记等，审核通过即可获得</p>
            </div>
            <div class="task-reward">+20 分/次</div>
          </div>
          
          <div class="task-card">
            <div class="task-icon bg-purple-soft"><IconMessageCircle class="text-purple" /></div>
            <div class="task-info">
              <h4>参与论坛讨论</h4>
              <p>在论坛发布有价值的帖子进行交流</p>
            </div>
            <div class="task-reward">+10 分/次</div>
          </div>
          
          <div class="task-card">
            <div class="task-icon bg-green-soft"><IconCheck class="text-green" /></div>
            <div class="task-info">
              <h4>每日登录签到</h4>
              <p>每天保持活跃，点击上方按钮签到</p>
            </div>
            <div class="task-reward">+5 分/天</div>
          </div>
        </div>
      </div>

      <div class="section-container">
        <div class="section-header">
          <h3 class="section-title">积分商城</h3>
          <span class="subtitle-small">使用积分兑换以下奖品</span>
        </div>
        
        <div class="prizes-grid">
          <div v-for="prize in prizes" :key="prize.id" class="prize-card card">
            <div class="prize-image-wrapper">
              <img v-if="prize.image_url" :src="prize.image_url" :alt="prize.name" class="prize-image" />
              <div v-else class="prize-placeholder">
                <IconGift class="placeholder-icon" />
              </div>
              <div class="stock-badge">库存: {{ prize.stock }}</div>
            </div>
            
            <div class="prize-body">
              <h4 class="prize-name">{{ prize.name }}</h4>
              <p class="prize-desc">{{ prize.description || '暂无描述' }}</p>
              
              <div class="prize-footer">
                <div class="prize-cost">
                  <IconStar class="cost-icon" />
                  <span>{{ prize.points_required }} 分</span>
                </div>
                <button 
                  @click="exchangePrize(prize)" 
                  class="btn btn-sm"
                  :class="getBtnClass(prize)"
                  :disabled="prize.stock <= 0 || userPoints < prize.points_required"
                >
                  {{ getBtnText(prize) }}
                </button>
              </div>
            </div>
          </div>

          <div v-if="prizes.length === 0" class="empty-state full-width card">
            <p>管理员还没上架任何奖品哦，敬请期待！</p>
          </div>
        </div>
      </div>
    </div>
  </template>

  <script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  import { useToast } from '../../composables/useToast'
  import { IconStar, IconUpload, IconMessageCircle, IconCalendar, IconCheck, IconGift } from '../icons'

  const toast = useToast()
  const userPoints = ref(0)
  const hasSigned = ref(false)
  const prizes = ref<any[]>([])
  const user = ref<any>(null)

  // 刷新用户信息以获取最新积分
  const fetchUserInfo = async () => {
    try {
      const token = localStorage.getItem('token')
      const res = await axios.get('http://127.0.0.1:8000/api/auth/profile/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      user.value = res.data
      userPoints.value = res.data.points || 0
      localStorage.setItem('user', JSON.stringify(res.data)) // 同步到本地
    } catch (error) {
      console.error('获取用户信息失败', error)
    }
  }

  // 获取商城奖品列表
  const fetchPrizes = async () => {
    try {
      const token = localStorage.getItem('token')
      const res = await axios.get('http://127.0.0.1:8000/api/points/prizes/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      prizes.value = res.data
    } catch (error) {
      console.error('获取奖品失败', error)
    }
  }

  // 获取签到状态 (这需要后端支持，这里做简单的本地模拟，如果你后端有签到接口请替换)
  const checkSignStatus = () => {
    const lastSign = localStorage.getItem('lastSignDate')
    const today = new Date().toDateString()
    hasSigned.value = lastSign === today
  }

  // 签到操作 (调用后端增分接口或本地模拟)
  const handleSign = async () => {
    if (hasSigned.value) return
    try {
      // 假设你有一个后端的签到/加分接口，如果没有，需要后端添加
      // await axios.post('http://127.0.0.1:8000/api/points/sign/', {}, { headers: ... })
      
      // 临时演示效果：直接前端加5分并记录
      userPoints.value += 5
      hasSigned.value = true
      localStorage.setItem('lastSignDate', new Date().toDateString())
      toast.success('签到成功！积分 +5')
    } catch (error) {
      toast.error('签到失败')
    }
  }

  // 兑换奖品按钮的文本和样式逻辑
  const getBtnText = (prize: any) => {
    if (prize.stock <= 0) return '已售罄'
    if (userPoints.value < prize.points_required) return '积分不足'
    return '立即兑换'
  }
  const getBtnClass = (prize: any) => {
    if (prize.stock <= 0) return 'btn-secondary'
    if (userPoints.value < prize.points_required) return 'btn-danger-outline'
    return 'btn-primary'
  }

  // 兑换奖品操作
  const exchangePrize = async (prize: any) => {
    if (!confirm(`确定要消耗 ${prize.points_required} 积分兑换【${prize.name}】吗？`)) return
    try {
      const token = localStorage.getItem('token')
      await axios.post('http://127.0.0.1:8000/api/points/exchange/', 
        { prize_id: prize.id }, 
        { headers: { Authorization: `Bearer ${token}` } }
      )
      toast.success('兑换成功！请联系管理员领取奖品。')
      fetchUserInfo() // 刷新积分
      fetchPrizes()   // 刷新库存
    } catch (error: any) {
      toast.error(error.response?.data?.error || '兑换失败，可能是库存不足或接口异常')
    }
  }

  onMounted(() => {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      user.value = JSON.parse(storedUser)
      userPoints.value = user.value.points || 0
    }
    fetchUserInfo()
    fetchPrizes()
    checkSignStatus()
  })
  </script>

  <style scoped>
  .page-container { padding: var(--spacing-lg); max-width: 1100px; margin: 0 auto; }
  .page-header { margin-bottom: var(--spacing-xl); }
  .page-header h2 { font-size: var(--font-size-3xl); font-weight: 600; color: var(--text-primary); margin-bottom: 8px; font-family: var(--font-sf); }
  .subtitle { color: var(--text-secondary); font-size: 15px; }

  .section-container { margin-top: 40px; }
  .section-header { display: flex; align-items: baseline; gap: 12px; margin-bottom: 20px; }
  .section-title { font-size: 20px; font-weight: 600; color: var(--text-primary); margin: 0; }
  .subtitle-small { font-size: 13px; color: var(--text-tertiary); }

  .card { background: var(--bg-primary); border-radius: var(--border-radius-xl); box-shadow: var(--shadow-sm); border: 1px solid var(--border-light); }

  /* 顶部概览卡片 */
  .points-overview-card { display: flex; justify-content: space-between; align-items: center; padding: 30px 40px; background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%); border-color: #fde68a; }
  .overview-left { display: flex; align-items: center; gap: 20px; }
  .points-icon-wrapper { width: 64px; height: 64px; background: linear-gradient(135deg, #f59e0b, #fbbf24); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 16px rgba(245, 158, 11, 0.2); }
  .huge-icon { width: 36px; height: 36px; color: white; }
  .points-text .label { font-size: 14px; color: var(--text-secondary); font-weight: 500; }
  .points-text .value { font-size: 48px; font-weight: 700; color: #d97706; margin: 0; line-height: 1; font-family: var(--font-sf); }

  /* 通用按钮 */
  .btn { display: flex; align-items: center; justify-content: center; gap: 8px; padding: 10px 20px; border-radius: var(--border-radius-md); font-weight: 500; cursor: pointer; border: none; transition: all 0.2s; }
  .btn-sm { padding: 8px 16px; font-size: 13px; border-radius: 6px; }
  .btn-primary { background: var(--primary-color); color: white; }
  .btn-primary:hover:not(:disabled) { background: var(--primary-dark); transform: translateY(-2px); }
  .btn-secondary { background: var(--bg-tertiary); color: var(--text-tertiary); cursor: not-allowed; }
  .btn-danger-outline { background: transparent; border: 1px solid #ef4444; color: #ef4444; cursor: not-allowed; }
  .btn-glow { box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3); }
  .btn-icon { width: 18px; height: 18px; }

  /* 任务网格 */
  .task-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }
  .task-card { background: var(--bg-primary); border-radius: var(--border-radius-lg); padding: 20px; border: 1px solid var(--border-light); display: flex; align-items: center; gap: 16px; transition: transform 0.2s; }
  .task-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-sm); border-color: var(--border-color); }
  .task-icon { width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
  .task-icon svg { width: 24px; height: 24px; }
  .bg-blue-soft { background: #e0f2fe; } .text-blue { color: #0284c7; }
  .bg-purple-soft { background: #f3e8ff; } .text-purple { color: #9333ea; }
  .bg-green-soft { background: #d1fae5; } .text-green { color: #059669; }
  .task-info { flex: 1; }
  .task-info h4 { margin: 0 0 4px; font-size: 15px; font-weight: 600; color: var(--text-primary); }
  .task-info p { margin: 0; font-size: 12px; color: var(--text-secondary); line-height: 1.4; }
  .task-reward { font-weight: 700; color: #f59e0b; font-size: 16px; white-space: nowrap; }

  /* 奖品网格 */
  .prizes-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 24px; margin-top: 20px; }
  .prize-card { display: flex; flex-direction: column; overflow: hidden; transition: all 0.3s; }
  .prize-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); border-color: var(--primary-light); }
  .prize-image-wrapper { position: relative; height: 160px; width: 100%; background: var(--bg-secondary); }
  .prize-image { width: 100%; height: 100%; object-fit: cover; }
  .prize-placeholder { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #f3f4f6, #e5e7eb); }
  .placeholder-icon { width: 48px; height: 48px; color: #9ca3af; }
  .stock-badge { position: absolute; top: 12px; right: 12px; background: rgba(0,0,0,0.6); color: white; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; backdrop-filter: blur(4px); }
  .prize-body { padding: 20px; display: flex; flex-direction: column; flex: 1; }
  .prize-name { margin: 0 0 8px; font-size: 16px; font-weight: 600; color: var(--text-primary); }
  .prize-desc { margin: 0 0 16px; font-size: 13px; color: var(--text-secondary); line-height: 1.5; flex: 1; }
  .prize-footer { display: flex; justify-content: space-between; align-items: center; margin-top: auto; padding-top: 16px; border-top: 1px dashed var(--border-light); }
  .prize-cost { display: flex; align-items: center; gap: 4px; color: #f59e0b; font-weight: 700; font-size: 16px; }
  .cost-icon { width: 18px; height: 18px; }
  .full-width { grid-column: 1 / -1; }
  .empty-state { padding: 60px; text-align: center; color: var(--text-tertiary); }

  .fade-in { animation: fadeIn var(--transition-normal); }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

  @media (max-width: 768px) {
    .points-overview-card { flex-direction: column; gap: 20px; text-align: center; }
    .overview-left { flex-direction: column; }
  }
  </style>