<template>
  <div class="ai-assistant-container">
    <!-- 聊天窗口 -->
    <transition name="slide">
      <div v-if="store.isOpen" class="chat-window">
        <div class="chat-header">
          <h3>AI 学习助手</h3>
          <div class="header-actions">
            <button @click="store.clearMessages" class="clear-btn" title="清空聊天记录">
              🗑️
            </button>
            <button @click="store.toggleOpen" class="close-btn">
              ✕
            </button>
          </div>
        </div>
        
        <div class="chat-messages" ref="messagesContainer">
          <div 
            v-for="(message, index) in store.messages" 
            :key="index"
            :class="['message', message.role]"
          >
            <div class="message-avatar">
              {{ message.role === 'user' ? '👤' : '🤖' }}
            </div>
            <div class="message-content">
              <div class="message-text">{{ message.content }}</div>
              <div class="message-time">{{ message.timestamp }}</div>
            </div>
          </div>
          <div v-if="store.isLoading" class="message ai">
            <div class="message-avatar">🤖</div>
            <div class="message-content">
              <div class="message-text">
                <div class="loading">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="chat-input-area">
          <input 
            v-model="userInput" 
            @keyup.enter="sendMessage" 
            placeholder="请输入您的问题..." 
            class="chat-input"
          />
          <button @click="sendMessage" class="send-btn" :disabled="!userInput.trim() || store.isLoading">
            发送
          </button>
        </div>
      </div>
    </transition>

    <!-- 浮动按钮 -->
    <transition name="bounce">
      <button v-if="!store.isOpen" class="float-button" @click="store.toggleOpen">
        <span class="button-icon">🤖</span>
        <span class="button-text">AI 助手</span>
      </button>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { useAIAssistantStore } from '../../stores/aiAssistant'
import axios from 'axios'

const store = useAIAssistantStore()
const userInput = ref('')
const messagesContainer = ref<HTMLElement | null>(null)

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
  bottom: 20px;
  right: 20px;
  z-index: 9999;
}

/* 浮动按钮 */
.float-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  transition: all 0.3s;
  font-size: 14px;
}

.float-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.6);
}

.button-icon {
  font-size: 18px;
}

.button-text {
  font-weight: 500;
}

/* 聊天窗口 */
.chat-window {
  position: fixed;
  bottom: 80px;
  right: 20px;
  width: 380px;
  height: 550px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.chat-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.clear-btn,
.close-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  font-size: 14px;
}

.clear-btn:hover,
.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

/* 消息区域 */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  background: #f5f7fa;
}

.message {
  display: flex;
  gap: 10px;
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
  font-size: 18px;
  flex-shrink: 0;
}

.message.user .message-avatar {
  background: #409eff;
  color: white;
}

.message.ai .message-avatar {
  background: #f0f0f0;
  color: #333;
}

.message-content {
  flex: 1;
}

.message-text {
  padding: 10px 15px;
  border-radius: 18px;
  line-height: 1.5;
  word-wrap: break-word;
}

.message.user .message-text {
  background: #409eff;
  color: white;
  border-bottom-right-radius: 4px;
}

.message.ai .message-text {
  background: white;
  color: #333;
  border-bottom-left-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.message-time {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
  text-align: right;
}

.message.user .message-time {
  text-align: left;
}

/* 加载动画 */
.loading {
  display: flex;
  gap: 4px;
}

.loading span {
  width: 8px;
  height: 8px;
  background: #409eff;
  border-radius: 50%;
  animation: loading 1.4s infinite ease-in-out both;
}

.loading span:nth-child(1) {
  animation-delay: -0.32s;
}

.loading span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes loading {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

/* 输入区域 */
.chat-input-area {
  display: flex;
  padding: 15px;
  border-top: 1px solid #e0e0e0;
  gap: 10px;
  background: white;
}

.chat-input {
  flex: 1;
  padding: 10px 16px;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
}

.chat-input:focus {
  border-color: #409eff;
}

.send-btn {
  padding: 0 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.send-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.send-btn:disabled {
  background: #c0c4cc;
  cursor: not-allowed;
  transform: none;
}

/* 动画 */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.slide-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.bounce-enter-active {
  animation: bounce-in 0.5s;
}

.bounce-leave-active {
  animation: bounce-in 0.5s reverse;
}

@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .chat-window {
    width: calc(100vw - 40px);
    height: calc(100vh - 200px);
    bottom: 80px;
    right: 20px;
  }
  
  .float-button {
    padding: 10px 16px;
  }
  
  .button-text {
    display: none;
  }
}
</style>
