import { ref, provide, inject } from 'vue'

interface Toast {
  id: number
  message: string
  type: 'success' | 'error' | 'warning' | 'info'
}

const toastKey = Symbol('toast')

export function createToast() {
  const toasts = ref<Toast[]>([])
  let toastId = 0

  const addToast = (message: string, type: 'success' | 'error' | 'warning' | 'info' = 'info') => {
    const id = ++toastId
    toasts.value.push({ id, message, type })
    
    setTimeout(() => {
      removeToast(id)
    }, 3000)
  }

  const removeToast = (id: number) => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }

  const toast = {
    toasts,
    addToast,
    removeToast,
    success: (msg: string) => addToast(msg, 'success'),
    error: (msg: string) => addToast(msg, 'error'),
    warning: (msg: string) => addToast(msg, 'warning'),
    info: (msg: string) => addToast(msg, 'info')
  }

  provide(toastKey, toast)
  return toast
}

export function useToast() {
  const toast = inject<ReturnType<typeof createToast>>(toastKey)
  if (!toast) {
    throw new Error('useToast must be used within a ToastProvider')
  }
  return toast
}
