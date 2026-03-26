<template>
  <div class="ai-assistant-container">
    <!-- 聊天窗口 -->
    <transition name="slide">
      <div v-if="store.isOpen" class="chat-window">
        <div class="chat-header">
          <div class="header-left">
            <div class="ai-avatar">
              <IconRobot class="ai-avatar-icon" />
            </div>
            <div class="header-info">
              <h3>AI 学习助手</h3>
              <span class="status-badge">
                <span class="status-dot"></span>
                在线
              </span>
            </div>
          </div>
          <div class="header-actions">
            <button @click="store.clearMessages" class="header-btn" title="清空聊天记录">
              <IconDelete class="header-btn-icon" />
            </button>
            <button @click="store.toggleOpen" class="header-btn" title="关闭">
              <IconClose class="header-btn-icon" />
            </button>
          </div>
        </div>
        
        <div class="chat-messages" ref="messagesContainer">
          <!-- 欢迎消息 -->
          <div v-if="store.messages.length === 0" class="welcome-message">
            <div class="welcome-icon">
              <IconSparkles class="sparkles-icon" />
            </div>
            <h4>你好！我是你的 AI 学习助手</h4>
            <p>我可以帮你解答学习问题、推荐课程资源、分析学习进度等</p>
            <div class="quick-actions">
              <button @click="sendQuickMessage('推荐一些学习资源')" class="quick-btn">
                <IconBook class="quick-btn-icon" />
                推荐资源
              </button>
              <button @click="sendQuickMessage('如何高效学习？')" class="quick-btn">
                <IconZap class="quick-btn-icon" />
                学习方法
              </button>
              <button @click="sendQuickMessage('分析我的学习情况')" class="quick-btn">
                <IconCollection class="quick-btn-icon" />
                学习分析
              </button>
            </div>
          </div>

          <div 
            v-for="(message, index) in store.messages" 
            :key="index"
            :class="['message', message.role]"
          >
            <div class="message-avatar">
              <IconUser v-if="message.role === 'user'" class="user-avatar-icon" />
              <IconRobot v-else class="ai-avatar-icon" />
            </div>
            <div class="message-content">
              <div class="message-bubble">
                <div class="message-text">{{ message.content }}</div>
              </div>
              <div class="message-time">{{ message.timestamp }}</div>
            </div>
          </div>
          
          <div v-if="store.isLoading" class="message ai">
            <div class="message-avatar">
              <IconRobot class="ai-avatar-icon" />
            </div>
            <div class="message-content">
              <div class="message-bubble">
                <div class="loading-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="chat-input-area">
          <div class="input-wrapper">
            <input 
              v-model="userInput" 
              @keyup.enter="sendMessage" 
              placeholder="请输入您的问题..." 
              class="chat-input"
            />
            <button 
              @click="sendMessage" 
              class="send-btn" 
              :disabled="!userInput.trim() || store.isLoading"
            >
              <IconSend class="send-icon" />
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- 浮动按钮 -->
    <transition name="bounce">
      <button v-if="!store.isOpen" class="float-button" @click="store.toggleOpen">
        <div class="float-button-inner">
          <IconRobot class="float-icon" />
          <span class="float-text">AI 助手</span>
        </div>
        <div class="float-button-glow"></div>
      </button>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { useAIAssistantStore } from '../../stores/aiAssistant'
import axios from 'axios'
import { 
  IconRobot, 
  IconDelete, 
  IconClose, 
  IconUser, 
  IconSparkles,
  IconBook,
  IconZap,
  IconCollection,
  IconSend
} from '../../components/icons'

const store = useAIAssistantStore()
const userInput = ref('')
const messagesContainer = ref<HTMLElement | null>(null)

const sendQuickMessage = (message: string) => {
  userInput.value = message
  sendMessage()
}

const sendMessage = async () => {
  if (!userInput.value.trim() || store.isLoading) return
  
  // 添加用户消息
  store.addUserMessage(userInput.value)
  
  // 清空输入框
  const input = userInput.value
  userInput.value = ''
  
  // 滚动到底部
  await nextTick()
  scrollToBottom()
  
  store.isLoading = true
  
  try {
    // 调用 AI API
    const response = await axios.post('http://127.0.0.1:8000/api/ai/chat/', {
      message: input
    }, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json'
      }
    })
    
    // 添加 AI 回复
    store.addAIMessage(response.data.response)
  } catch (error) {
    console.error('AI API 调用失败:', error)
    // 添加错误消息
    store.addAIMessage('抱歉，AI 服务暂时不可用，请稍后再试。')
  } finally {
    store.isLoading = false
    
    // 滚动到底部
    await nextTick()
    scrollToBottom()
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}
</script>

<style scoped>
.ai-assistant-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
}

/* 聊天窗口 */
.chat-window {
  position: fixed;
  bottom: 100px;
  right: 24px;
  width: 400px;
  height: 600px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.08);
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
  color: white;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.ai-avatar {
  width: 44px;
  height: 44px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
}

.ai-avatar-icon {
  width: 24px;
  height: 24px;
  color: white;
}

.header-info h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
  margin-top: 2px;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.header-actions {
  display: flex;
  gap: 8px;
}

.header-btn {
  width: 36px;
  height: 36px;
  background: rgba(255, 255, 255, 0.15);
  border: none;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  color: white;
}

.header-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: scale(1.05);
}

.header-btn-icon {
  width: 18px;
  height: 18px;
}

/* 消息区域 */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: #f8fafc;
}

/* 欢迎消息 */
.welcome-message {
  text-align: center;
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.welcome-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px rgba(13, 148, 136, 0.3);
}

.sparkles-icon {
  width: 32px;
  height: 32px;
  color: white;
}

.welcome-message h4 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.welcome-message p {
  margin: 0;
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-top: 8px;
}

.quick-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: white;
  border: 1px solid var(--border-color);
  border-radius: 20px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  transition: all 0.3s;
}

.quick-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
  background: rgba(13, 148, 136, 0.05);
  transform: translateY(-1px);
}

.quick-btn-icon {
  width: 16px;
  height: 16px;
}

/* 消息样式 */
.message {
  display: flex;
  gap: 12px;
  max-width: 85%;
}

.message.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message.ai {
  align-self: flex-start;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message.user .message-avatar {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
}

.message.ai .message-avatar {
  background: white;
  border: 2px solid var(--border-color);
}

.user-avatar-icon {
  width: 20px;
  height: 20px;
  color: white;
}

.ai-avatar-icon {
  width: 20px;
  height: 20px;
  color: var(--primary-color);
}

.message-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.message-bubble {
  padding: 12px 16px;
  border-radius: 18px;
  line-height: 1.6;
  word-wrap: break-word;
}

.message.user .message-bubble {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  color: white;
  border-bottom-right-radius: 4px;
}

.message.ai .message-bubble {
  background: white;
  color: var(--text-primary);
  border-bottom-left-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid var(--border-light);
}

.message-time {
  font-size: 11px;
  color: var(--text-tertiary);
  margin-top: 2px;
}

.message.user .message-time {
  text-align: right;
}

/* 加载动画 */
.loading-dots {
  display: flex;
  gap: 4px;
  padding: 4px 8px;
}

.loading-dots span {
  width: 8px;
  height: 8px;
  background: var(--primary-color);
  border-radius: 50%;
  animation: loading-bounce 1.4s infinite ease-in-out both;
}

.loading-dots span:nth-child(1) {
  animation-delay: -0.32s;
}

.loading-dots span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes loading-bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

/* 输入区域 */
.chat-input-area {
  padding: 16px 20px;
  border-top: 1px solid var(--border-light);
  background: white;
}

.input-wrapper {
  display: flex;
  gap: 12px;
  align-items: center;
  background: #f1f5f9;
  border-radius: 24px;
  padding: 6px 6px 6px 20px;
}

.chat-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
  background: transparent;
  color: var(--text-primary);
}

.chat-input::placeholder {
  color: var(--text-tertiary);
}

.send-btn {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  color: white;
  box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3);
}

.send-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(13, 148, 136, 0.4);
}

.send-btn:disabled {
  background: var(--text-tertiary);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.send-icon {
  width: 18px;
  height: 18px;
}

/* 浮动按钮 */
.float-button {
  position: relative;
  padding: 0;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
}

.float-button-inner {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 24px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
  color: white;
  border-radius: 30px;
  box-shadow: 0 8px 20px rgba(13, 148, 136, 0.4);
  transition: all 0.3s;
  position: relative;
  z-index: 1;
}

.float-button:hover .float-button-inner {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(13, 148, 136, 0.5);
}

.float-icon {
  width: 22px;
  height: 22px;
}

.float-text {
  font-weight: 600;
  font-size: 15px;
}

.float-button-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  border-radius: 30px;
  filter: blur(20px);
  opacity: 0.4;
  z-index: 0;
  animation: glow-pulse 2s ease-in-out infinite;
}

@keyframes glow-pulse {
  0%, 100% { opacity: 0.4; transform: translate(-50%, -50%) scale(1); }
  50% { opacity: 0.6; transform: translate(-50%, -50%) scale(1.05); }
}

/* 动画 */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

.slide-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

.bounce-enter-active {
  animation: bounce-in 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.bounce-leave-active {
  animation: bounce-in 0.5s cubic-bezier(0.4, 0, 0.2, 1) reverse;
}

@keyframes bounce-in {
  0% {
    opacity: 0;
    transform: scale(0);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .chat-window {
    width: calc(100vw - 48px);
    height: calc(100vh - 200px);
    bottom: 90px;
    right: 24px;
  }
  
  .float-button-inner {
    padding: 12px 18px;
  }
  
  .float-text {
    display: none;
  }
  
  .quick-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .quick-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>