<template>
  <div class="toast-container">
    <TransitionGroup name="toast-list">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="['toast', `toast-${toast.type}`]"
        @click="removeToast(toast.id)"
      >
        <component :is="getIcon(toast.type)" class="toast-icon" />
        <span class="toast-message">{{ toast.message }}</span>
        <button class="toast-close" @click.stop="removeToast(toast.id)">
          <IconClose />
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup lang="ts">
import { useToast } from '../../composables/useToast'
import { IconCheck, IconAlertCircle, IconInfo, IconWarning, IconClose } from '../icons'

const { toasts, removeToast } = useToast()

const getIcon = (type: string) => {
  const icons: any = {
    success: IconCheck,
    error: IconAlertCircle,
    warning: IconWarning,
    info: IconInfo
  }
  return icons[type] || IconInfo
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 12px;
  pointer-events: none;
}

.toast {
  pointer-events: auto;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 24px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  min-width: 300px;
  max-width: 500px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  animation: slideIn 0.3s ease;
}

.toast::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
}

.toast-success::before { background: #10b981; }
.toast-error::before { background: #ef4444; }
.toast-warning::before { background: #f59e0b; }
.toast-info::before { background: #3b82f6; }

.toast-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.toast-success .toast-icon { color: #10b981; }
.toast-error .toast-icon { color: #ef4444; }
.toast-warning .toast-icon { color: #f59e0b; }
.toast-info .toast-icon { color: #3b82f6; }

.toast-message {
  flex: 1;
  font-size: 15px;
  font-weight: 500;
  color: #1f2937;
  line-height: 1.5;
}

.toast-close {
  width: 24px;
  height: 24px;
  border: none;
  background: transparent;
  color: #9ca3af;
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}

.toast-close:hover {
  background: #f3f4f6;
  color: #4b5563;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.toast-list-enter-active,
.toast-list-leave-active {
  transition: all 0.3s ease;
}

.toast-list-enter-from,
.toast-list-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}
</style>
