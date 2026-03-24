import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface Message {
  role: 'user' | 'ai'
  content: string
  timestamp: string
}

export const useAIAssistantStore = defineStore('aiAssistant', () => {
  const isOpen = ref(false)
  const isLoading = ref(false)
  const messages = ref<Message[]>([
    {
      role: 'ai',
      content: '你好！我是你的 AI 学习助手，有什么可以帮助你的吗？',
      timestamp: new Date().toLocaleTimeString()
    }
  ])

  // 从 localStorage 加载聊天记录
  const loadMessages = () => {
    const saved = localStorage.getItem('ai_messages')
    if (saved) {
      try {
        messages.value = JSON.parse(saved)
      } catch (e) {
        console.error('加载聊天记录失败', e)
      }
    }
  }

  // 保存聊天记录到 localStorage
  const saveMessages = () => {
    localStorage.setItem('ai_messages', JSON.stringify(messages.value))
  }

  // 添加用户消息
  const addUserMessage = (content: string) => {
    const message: Message = {
      role: 'user',
      content,
      timestamp: new Date().toLocaleTimeString()
    }
    messages.value.push(message)
    saveMessages()
  }

  // 添加 AI 回复
  const addAIMessage = (content: string) => {
    const message: Message = {
      role: 'ai',
      content,
      timestamp: new Date().toLocaleTimeString()
    }
    messages.value.push(message)
    saveMessages()
  }

  // 清空聊天记录
  const clearMessages = () => {
    messages.value = [{
      role: 'ai',
      content: '你好！我是你的 AI 学习助手，有什么可以帮助你的吗？',
      timestamp: new Date().toLocaleTimeString()
    }]
    saveMessages()
  }

  // 切换开关状态
  const toggleOpen = () => {
    isOpen.value = !isOpen.value
    if (isOpen.value && messages.value.length === 0) {
      loadMessages()
    }
  }

  // 初始化
  loadMessages()

  return {
    isOpen,
    isLoading,
    messages,
    addUserMessage,
    addAIMessage,
    clearMessages,
    toggleOpen
  }
})
