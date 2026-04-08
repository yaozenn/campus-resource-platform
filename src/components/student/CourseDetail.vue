<template>
  <div class="page-container fade-in">
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>正在全力加载资源信息...</p>
    </div>
    
    <div v-else-if="!course" class="empty-state">
      <IconFolder class="empty-icon" />
      <p>哎呀，该资源不存在或已被下架</p>
      <button @click="goBack" class="btn btn-primary mt-4">返回列表</button>
    </div>
    
    <div v-else class="detail-page">
      <div class="back-btn" @click="goBack">
        <IconArrowLeft class="btn-icon" /> <span>返回资源大厅</span>
      </div>
      
      <div class="detail-content">
        <div class="detail-left">
          <div class="media-section card">
            
            <div v-if="isVideo && !isPreviewing" class="video-player">
              <video 
                :src="course.file_url" 
                controls 
                class="video-element"
                :poster="course.cover_image"
                controlsList="nodownload"
              >
                您的浏览器不支持视频播放
              </video>
            </div>

            <div v-else-if="isPreviewing" class="preview-container">
              <div class="preview-header">
                <span>正在预览文档内容...</span>
                <button @click="isPreviewing = false" class="btn-close-preview">关闭预览</button>
              </div>
              <iframe :src="course.file_url" class="preview-iframe" title="文档预览"></iframe>
            </div>
            
            <div v-else class="cover-display" :class="getCoverClassByMain(course.type_name)">
              <div class="cover-overlay"></div>
              <div class="cover-content">
                <component :is="getCoverIconComponent(course.type_name)" class="cover-icon" />
                <span class="cover-text">{{ course.type_name || '未分类资源' }}</span>
              </div>
              <div v-if="course.is_second_hand" class="second-hand-badge">二手闲置 ¥{{ course.price }}</div>
            </div>
            
            <div class="action-toolbar">
              <button v-if="!isVideo && !isPreviewing" @click="togglePreview" class="btn-action btn-outline-primary">
                <IconEye class="action-icon" /> 免费预览
              </button>
              <button v-if="isPreviewing" @click="isPreviewing = false" class="btn-action btn-outline-primary">
                <IconArrowLeft class="action-icon" /> 退出预览
              </button>

              <button @click="downloadCourse" class="btn-action btn-primary">
                <IconDownload class="action-icon" /> 下载原件
              </button>
              <button @click="toggleCollect" :class="['btn-action', isCollected ? 'btn-success' : 'btn-outline']">
                <IconHeart class="action-icon" :filled="isCollected" /> 
                {{ isCollected ? '已收藏' : '加入收藏' }}
              </button>
            </div>
          </div>
          
          <div class="comments-section card">
            <h3 class="section-title">
              <IconMessageCircle class="section-title-icon" /> 讨论交流 ({{ comments.length }})
            </h3>
            
            <div class="comment-form">
              <textarea 
                v-model="newComment" 
                placeholder="这份资料对你有帮助吗？说点什么吧..." 
                class="input"
                rows="3"
              ></textarea>
              <div class="comment-actions">
                <button @click="submitComment" class="btn btn-primary" :disabled="submitting">
                  {{ submitting ? '发送中...' : '发表评论' }}
                </button>
              </div>
            </div>
            
            <div class="comments-list">
              <div v-for="comment in comments" :key="comment.id" class="comment-item">
                <div class="avatar-circle">
                  {{ comment.user?.name?.charAt(0) || comment.user?.username?.charAt(0) || 'U' }}
                </div>
                <div class="comment-body">
                  <div class="comment-header">
                    <span class="comment-author">{{ comment.user?.name || comment.user?.username }}</span>
                    <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
                  </div>
                  <p class="comment-content">{{ comment.content }}</p>
                </div>
              </div>
              <div v-if="comments.length === 0" class="empty-state-small">
                暂无评论，快来抢下首评吧！
              </div>
            </div>
          </div>
        </div>
        
        <div class="detail-right">
          <div class="info-card card">
            <h1 class="course-title">{{ course.title }}</h1>
            
            <div class="rating-display">
              <div class="stars">
                <IconStar 
                  v-for="star in 5" 
                  :key="star" 
                  @click="submitRating(star)"
                  class="star-item"
                  :class="{ active: star <= (userRating || course.rating || 0) }"
                  title="点击打分"
                />
              </div>
              <span class="rating-text">
                {{ course.rating ? `${course.rating} 分` : '暂无评分' }} 
                <span class="rating-hint">(点击星星打分)</span>
              </span>
            </div>
            
            <div class="course-meta-grid">
              <div class="meta-item">
                <span class="meta-label">资源分类</span>
                <span class="meta-value tag-blue">{{ course.type_name || '未分类' }}</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">上传作者</span>
                <span class="meta-value">{{ course.uploader_name || course.uploader_username || course.uploader_info?.name || course.uploader_info?.username || course.uploader?.name || course.uploader?.username }}</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">下载热度</span>
                <span class="meta-value text-orange">{{ course.downloads }} 次</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">上传时间</span>
                <span class="meta-value">{{ formatTime(course.upload_date).split(' ')[0] }}</span>
              </div>
            </div>
            
            <div class="course-description">
              <h3>
                <IconBookOpen class="section-icon" /> 资源描述
              </h3>
              <p>{{ course.description || '这位同学很懒，没有留下详细描述~' }}</p>
            </div>

            <div class="report-wrapper">
              <button @click="showReportModal = true" class="btn-report">
                <IconAlertCircle class="report-icon" /> 发现违规、侵权或低俗内容？点击举报
              </button>
            </div>
            
            <div v-if="relatedCourses.length > 0" class="related-section">
              <h3 class="section-title-small">
                <IconBook class="section-icon" /> 猜你需要
              </h3>
              <div class="related-list">
                <div v-for="related in relatedCourses" :key="related.id" class="related-item" @click="viewCourse(related.id)">
                  <component :is="getCoverIconComponent(related.type_name)" class="related-icon" />
                  <div class="related-info">
                    <h4 class="text-truncate">{{ related.title }}</h4>
                    <p>{{ related.downloads }} 次下载</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showReportModal" class="modal-overlay" @click="showReportModal = false">
      <div class="modal-card slide-up" @click.stop>
        <div class="modal-header">
          <h3>
            <IconAlertCircle class="modal-icon" /> 举报该资源
          </h3>
          <button @click="showReportModal = false" class="btn-close-icon">
            <IconClose class="close-icon" />
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>举报类型</label>
            <select v-model="reportData.reason_type" class="input">
              <option value="侵权">涉嫌侵权（未经授权分享）</option>
              <option value="广告">垃圾广告 / 违规引流</option>
              <option value="违法">违法违规 / 政治敏感</option>
              <option value="低俗">低俗色情</option>
              <option value="其他">其他原因</option>
            </select>
          </div>
          <div class="form-group mt-3">
            <label>详细说明（选填）</label>
            <textarea v-model="reportData.details" class="input" rows="3" placeholder="请简要描述违规情况，方便管理员核实..."></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showReportModal = false" class="btn btn-secondary">取消</button>
          <button @click="submitReport" class="btn btn-danger">提交举报</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { formatTime } from '../../utils/timeFormat'
import { useToast } from '../../composables/useToast'
import { 
  IconArrowLeft, IconDownload, IconEye, IconHeart, IconStar, 
  IconMessageCircle, IconBookOpen, IconAlertCircle, IconFolder,
  IconDocument, IconVideo, IconFile, IconClose, IconBook
} from '../../components/icons'

const toast = useToast()

const route = useRoute()
const router = useRouter()

const course = ref<any>(null)
const loading = ref(true)
const isCollected = ref(false)
const comments = ref<any[]>([])
const newComment = ref('')
const submitting = ref(false)
const relatedCourses = ref<any[]>([])

// 高级功能状态
const isPreviewing = ref(false)
const userRating = ref(0)
const showReportModal = ref(false)
const reportData = ref({ reason_type: '侵权', details: '' })

const courseId = computed(() => route.params.id as string)

const isVideo = computed(() => {
  const videoTypes = ['视频', '网络课程', '优质网课链接']
  return course.value && videoTypes.includes(course.value.type_name || course.value.type?.name)
})

// UI 辅助函数
const getCoverIconComponent = (typeName: string) => {
  if (!typeName) return IconFolder
  if (typeName.includes('课件') || typeName.includes('笔记')) return IconDocument
  if (typeName.includes('视频') || typeName.includes('链接')) return IconVideo
  if (typeName.includes('书') || typeName.includes('资料')) return IconBook
  if (typeName.includes('真题') || typeName.includes('报告')) return IconFile
  return IconFolder
}

const getCoverClassByMain = (typeName: string) => {
  if (!typeName) return 'bg-gradient-gray'
  if (typeName.includes('课件') || typeName.includes('笔记')) return 'bg-gradient-teal'
  if (typeName.includes('视频') || typeName.includes('链接')) return 'bg-gradient-blue'
  return 'bg-gradient-purple'
}

// 核心数据获取
const fetchCourseDetail = async () => {
  loading.value = true
  isPreviewing.value = false
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/courses/${courseId.value}/`)
    course.value = response.data
    // 如果后端还没有rating字段，前端容错给个0
    if (typeof course.value.rating === 'undefined') course.value.rating = 0 
  } catch (error) {
    console.error('获取资源详情失败', error)
  } finally {
    loading.value = false
  }
}

const fetchComments = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/courses/${courseId.value}/comments/`)
    comments.value = response.data
  } catch (error) { console.error('获取评论失败', error) }
}

const fetchRelatedCourses = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/courses/')
    const allCourses = response.data
    relatedCourses.value = allCourses
      .filter((c: any) => c.status === 'active' && c.type === course.value?.type && c.id !== course.value?.id)
      .slice(0, 4)
  } catch (error) { console.error('获取相关资源失败') }
}

// 用户交互行为
const togglePreview = () => {
  if (!course.value?.file_url) return toast.warning('该资源暂无文件链接，无法预览')
  isPreviewing.value = true
}

const submitRating = async (star: number) => {
  userRating.value = star
  try {
    const token = localStorage.getItem('token')
    const response = await axios.post(
      `http://127.0.0.1:8000/api/courses/${courseId.value}/rate/`,
      { rating: star },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    
    // 更新显示的评分
    if (response.data.rating) {
      course.value.rating = response.data.rating
    }
    
    toast.success(`感谢评分！你给出了 ${star} 星。`)
  } catch (error) {
    toast.error('评分失败，请稍后再试')
  }
}

const submitReport = async () => {
  try {
    const token = localStorage.getItem('token')
    await axios.post(
      `http://127.0.0.1:8000/api/courses/${courseId.value}/report/`,
      reportData.value,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    
    toast.success('举报已提交！管理员将会在24小时内进行核实处理。')
    showReportModal.value = false
    reportData.value = { reason_type: '侵权', details: '' }
  } catch (error) {
    toast.error('提交举报失败')
  }
}

const submitComment = async () => {
  console.log('submitComment called, newComment:', newComment.value)
  if (!newComment.value.trim()) {
    toast.warning('请输入评论内容')
    return
  }
  submitting.value = true
  try {
    const token = localStorage.getItem('token')
    console.log('Token:', token ? 'exists' : 'missing')
    console.log('Course ID:', courseId.value)
    const response = await axios.post(`http://127.0.0.1:8000/api/courses/${courseId.value}/comments/`, 
      { content: newComment.value, user_rating: 5 }, 
      { headers: { Authorization: `Bearer ${token}` } }
    )
    console.log('Comment posted successfully:', response.data)
    newComment.value = ''
    await fetchComments()
    toast.success('评论成功！')
  } catch (error: any) {
    console.error('评论错误:', error)
    console.error('错误详情:', error.response?.data)
    console.error('错误状态码:', error.response?.status)
    toast.error('评论失败：' + (error.response?.data?.detail || error.response?.data?.error || JSON.stringify(error.response?.data) || error.message || '未知错误'))
  } finally {
    submitting.value = false
    console.log('submitComment finished')
  }
}

const checkCollection = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/api/courses/collections/', { headers: { Authorization: `Bearer ${token}` } })
    isCollected.value = response.data.some((c: any) => c.resource?.id === course.value?.id)
  } catch (error) {}
}

const toggleCollect = async () => {
  try {
    const token = localStorage.getItem('token')
    if (isCollected.value) {
      const collection = await axios.get('http://127.0.0.1:8000/api/courses/collections/', { headers: { Authorization: `Bearer ${token}` } })
      const target = collection.data.find((c: any) => c.resource?.id === course.value?.id)
      if (target) await axios.delete(`http://127.0.0.1:8000/api/courses/uncollect/${target.id}/`, { headers: { Authorization: `Bearer ${token}` } })
      isCollected.value = false
    } else {
      await axios.post('http://127.0.0.1:8000/api/courses/collect/', { resource: course.value?.id }, { headers: { Authorization: `Bearer ${token}` } })
      isCollected.value = true
    }
  } catch (error: any) { toast.error('操作失败') }
}

const downloadCourse = async () => {
  if (!course.value?.file_url) return toast.warning('该资源暂无下载链接')
  try {
    const token = localStorage.getItem('token')
    await axios.post(`http://127.0.0.1:8000/api/courses/${course.value.id}/download/`, {}, { headers: { Authorization: `Bearer ${token}` } })
    course.value.downloads += 1
    
    const link = document.createElement('a')
    link.href = course.value.file_url
    link.target = '_blank'
    link.download = course.value.title || 'download'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (error: any) {
    toast.error(error.response?.data?.error || '下载失败')
  }
}

const goBack = () => router.push('/student/courses')
const viewCourse = (id: string) => router.push(`/student/courses/${id}`)

// 监听路由参数变化（用于点击右侧相关资源时刷新页面）
watch(courseId, () => {
  if(courseId.value) {
    fetchCourseDetail()
    fetchComments()
    checkCollection()
    fetchRelatedCourses()
  }
})

onMounted(() => {
  fetchCourseDetail()
  fetchComments()
  checkCollection()
  fetchRelatedCourses()
})
</script>

<style scoped>
/* 基础与布局 */
.page-container { padding: var(--spacing-lg); max-width: 1200px; margin: 0 auto; min-height: 100vh; }
.card { background: var(--bg-primary); border-radius: var(--border-radius-xl); box-shadow: var(--shadow-sm); border: 1px solid var(--border-light); overflow: hidden; }
.back-btn { display: inline-flex; align-items: center; gap: 8px; margin-bottom: 24px; color: var(--text-secondary); cursor: pointer; font-weight: 500; font-size: 15px; transition: color 0.2s; }
.back-btn:hover { color: var(--primary-color); }

.detail-content { display: grid; grid-template-columns: 1.8fr 1fr; gap: 30px; }
.detail-left { display: flex; flex-direction: column; gap: 30px; }
.detail-right { display: flex; flex-direction: column; position: sticky; top: 80px; height: fit-content; }

/* 媒体区域 (视频/封面/预览) */
.media-section { display: flex; flex-direction: column; }
.video-player { width: 100%; background: #000; border-radius: var(--border-radius-xl) var(--border-radius-xl) 0 0; }
.video-element { width: 100%; max-height: 500px; display: block; }

.preview-container { width: 100%; height: 500px; display: flex; flex-direction: column; background: #f3f4f6; }
.preview-header { padding: 10px 20px; background: #374151; color: white; display: flex; justify-content: space-between; align-items: center; font-size: 14px; }
.btn-close-preview { background: #ef4444; color: white; border: none; padding: 4px 12px; border-radius: 4px; cursor: pointer; }
.preview-iframe { flex: 1; border: none; width: 100%; background: white; }

.cover-display { width: 100%; height: 400px; position: relative; display: flex; align-items: center; justify-content: center; }
.bg-gradient-teal { background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%); }
.bg-gradient-blue { background: linear-gradient(135deg, #0ea5e9 0%, #38bdf8 100%); }
.bg-gradient-purple { background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%); }
.bg-gradient-gray { background: linear-gradient(135deg, #6b7280 0%, #9ca3af 100%); }

.cover-overlay { position: absolute; inset: 0; background: linear-gradient(to bottom, transparent 0%, rgba(0,0,0,0.4) 100%); }
.cover-content { position: relative; z-index: 1; display: flex; flex-direction: column; align-items: center; gap: 16px; }
.cover-icon { width: 96px; height: 96px; color: white; filter: drop-shadow(0 4px 12px rgba(0,0,0,0.2)); }
.cover-text { color: white; font-size: 16px; font-weight: 600; padding: 6px 20px; background: rgba(255,255,255,0.2); backdrop-filter: blur(8px); border-radius: 20px; }
.second-hand-badge { position: absolute; top: 20px; right: 20px; background: #f59e0b; color: white; padding: 8px 16px; border-radius: 8px; font-weight: 700; font-size: 16px; z-index: 2; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }

/* 操作工具栏 */
.action-toolbar { display: flex; padding: 20px; gap: 16px; background: var(--bg-primary); border-top: 1px solid var(--border-light); }
.btn-action { 
  flex: 1; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  gap: 8px; 
  padding: 14px 20px; 
  border-radius: var(--border-radius-lg); 
  font-weight: 600; 
  font-size: 15px; 
  cursor: pointer; 
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); 
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
}
.btn-action::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
  opacity: 0;
  transition: opacity 0.3s;
}
.btn-action:hover::before {
  opacity: 1;
}
.action-icon { width: 20px; height: 20px; transition: transform 0.3s; }
.btn-action:hover .action-icon {
  transform: scale(1.1);
}
.btn-primary { 
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%); 
  color: white;
  box-shadow: 0 4px 14px rgba(13, 148, 136, 0.3);
}
.btn-primary:hover { 
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-color) 100%);
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(13, 148, 136, 0.4);
}
.btn-outline-primary { 
  background: transparent; 
  border-color: var(--primary-color); 
  color: var(--primary-color);
  box-shadow: 0 2px 8px rgba(13, 148, 136, 0.1);
}
.btn-outline-primary:hover { 
  background: var(--primary-soft);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(13, 148, 136, 0.2);
}
.btn-success { 
  background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
  color: white;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);
}
.btn-success:hover {
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
}
.btn-outline { 
  background: transparent; 
  border-color: var(--border-color); 
  color: var(--text-secondary);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
.btn-outline:hover { 
  border-color: var(--primary-color); 
  color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(13, 148, 136, 0.15);
}

.empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 40px; }
.empty-icon { width: 80px; height: 80px; color: var(--text-tertiary); margin-bottom: 16px; }

.section-title { font-size: 18px; font-weight: 600; margin: 0 0 20px; display: flex; align-items: center; gap: 8px; }
.section-title-icon { width: 20px; height: 20px; }

.section-icon { width: 18px; height: 18px; margin-right: 6px; }

.stars { display: flex; gap: 4px; }
.star-item { width: 24px; height: 24px; color: #d1d5db; cursor: pointer; transition: color 0.2s; }
.star-item.active, .star-item:hover { color: #f59e0b; fill: #f59e0b; }

.related-icon { width: 24px; height: 24px; background: white; color: var(--primary-color); }

.report-icon { width: 16px; height: 16px; margin-right: 4px; }

.modal-header { padding: 20px 24px; border-bottom: 1px solid var(--border-light); display: flex; justify-content: space-between; align-items: center; background: #fff1f2; }
.modal-header h3 { margin: 0; font-size: 16px; color: #e11d48; font-weight: 600; display: flex; align-items: center; gap: 8px; }
.modal-icon { width: 20px; height: 20px; }
.btn-close-icon { background: none; border: none; cursor: pointer; padding: 4px; }
.close-icon { width: 20px; height: 20px; color: #f43f5e; }

/* 右侧信息面板 */
.info-card { padding: 30px; }
.course-title { font-size: 24px; font-weight: 700; color: var(--text-primary); margin: 0 0 16px; line-height: 1.4; }

/* 星级评分 */
.rating-display { display: flex; align-items: center; gap: 12px; margin-bottom: 24px; padding-bottom: 20px; border-bottom: 1px dashed var(--border-light); }
.rating-text { font-size: 16px; font-weight: 700; color: #f59e0b; }
.rating-hint { font-size: 12px; color: var(--text-tertiary); font-weight: 400; margin-left: 8px; }

/* 元信息网格 */
.course-meta-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 30px; }
.meta-item { display: flex; flex-direction: column; gap: 4px; }
.meta-label { font-size: 12px; color: var(--text-tertiary); }
.meta-value { font-size: 14px; font-weight: 500; color: var(--text-primary); }
.tag-blue { background: #e0f2fe; color: #0284c7; padding: 2px 8px; border-radius: 4px; width: fit-content; }
.text-orange { color: #d97706; }

/* 描述与举报 */
.course-description h3 { font-size: 16px; font-weight: 600; margin: 0 0 12px; display: flex; align-items: center; }
.course-description p { color: var(--text-secondary); font-size: 14px; line-height: 1.6; margin: 0; background: var(--bg-secondary); padding: 16px; border-radius: var(--border-radius-md); }
.report-wrapper { margin-top: 24px; text-align: center; }
.btn-report { background: transparent; border: none; color: var(--text-tertiary); font-size: 13px; text-decoration: underline; cursor: pointer; transition: color 0.2s; display: inline-flex; align-items: center; }
.btn-report:hover { color: #ef4444; }

/* 猜你需要 (相关资源) */
.related-section { margin-top: 30px; padding-top: 24px; border-top: 1px solid var(--border-light); }
.section-title-small { font-size: 16px; font-weight: 600; margin: 0 0 16px; display: flex; align-items: center; }
.related-list { display: flex; flex-direction: column; gap: 12px; }
.related-item { display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--bg-secondary); border-radius: var(--border-radius-md); cursor: pointer; transition: all 0.2s; }
.related-item:hover { background: var(--bg-tertiary); border: 1px solid var(--primary-light); }
.related-info h4 { margin: 0 0 4px; font-size: 14px; font-weight: 500; color: var(--text-primary); }
.related-info p { margin: 0; font-size: 12px; color: var(--text-secondary); }
.text-truncate { display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden; }

/* 评论区 */
.comments-section { padding: 30px; }
.input { width: 100%; padding: 12px; border: 1px solid var(--border-color); border-radius: var(--border-radius-md); font-size: 14px; background: var(--bg-secondary); outline: none; transition: all 0.2s; }
.input:focus { border-color: var(--primary-color); background: var(--bg-primary); }
.comment-actions { display: flex; justify-content: flex-end; margin-top: 12px; margin-bottom: 30px; }
.comment-item { display: flex; gap: 16px; padding-bottom: 20px; border-bottom: 1px solid var(--border-light); margin-bottom: 20px; }
.comment-item:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
.avatar-circle { width: 40px; height: 40px; border-radius: 50%; background: var(--primary-soft); color: var(--primary-dark); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 16px; }
.comment-header { display: flex; justify-content: space-between; margin-bottom: 8px; }
.comment-author { font-weight: 600; font-size: 14px; color: var(--text-primary); }
.comment-time { font-size: 12px; color: var(--text-tertiary); }
.comment-content { margin: 0; font-size: 14px; color: var(--text-secondary); line-height: 1.5; }
.empty-state-small { text-align: center; color: var(--text-tertiary); padding: 20px; font-size: 14px; }

/* 弹窗样式 */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 2000; }
.modal-card { background: var(--bg-primary); width: 100%; max-width: 440px; border-radius: var(--border-radius-xl); box-shadow: var(--shadow-xl); overflow: hidden; }
.modal-body { padding: 24px; }
.form-group { display: flex; flex-direction: column; gap: 8px; }
.form-group label { font-size: 14px; font-weight: 500; color: var(--text-secondary); }
.mt-3 { margin-top: 16px; }
.modal-footer { padding: 16px 24px; background: var(--bg-secondary); display: flex; justify-content: flex-end; gap: 12px; }
.btn { padding: 8px 20px; border-radius: 6px; font-size: 14px; font-weight: 500; border: none; cursor: pointer; transition: all 0.2s; }
.btn-secondary { background: #e5e7eb; color: #4b5563; }
.btn-secondary:hover { background: #d1d5db; }
.btn-danger { background: #ef4444; color: white; }
.btn-danger:hover { background: #dc2626; }

/* 动画 */
.fade-in { animation: fadeIn 0.3s ease; }
.slide-up { animation: slideUp 0.3s ease; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

/* 响应式 */
@media (max-width: 860px) {
  .detail-content { grid-template-columns: 1fr; }
  .detail-right { position: static; }
  .action-toolbar { flex-wrap: wrap; }
}
</style>