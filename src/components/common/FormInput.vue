<template>
  <div class="form-input-wrapper">
    <label v-if="label" class="form-label">
      {{ label }}
      <span v-if="required" class="required">*</span>
    </label>
    
    <div class="form-input-container" :class="{ 'has-error': error }">
      <input
        v-model="inputValue"
        :type="inputType"
        :placeholder="placeholder"
        :class="['form-input', { 'has-error': error }]"
        :disabled="disabled"
        @blur="handleBlur"
        @input="handleInput"
      />
      
      <!-- 显示/隐藏密码按钮 -->
      <button
        v-if="type === 'password'"
        type="button"
        class="toggle-password"
        @click="showPassword = !showPassword"
      >
        <IconEye v-if="!showPassword" class="toggle-icon" />
        <IconEyeOff v-else class="toggle-icon" />
      </button>
      
      <!-- 错误图标 -->
      <IconAlertCircle v-if="error" class="error-icon" />
    </div>
    
    <!-- 错误提示 -->
    <transition name="fade">
      <div v-if="error" class="error-message">
        <IconAlertCircle class="error-icon-small" />
        {{ error }}
      </div>
    </transition>
    
    <!-- 密码强度指示器 -->
    <PasswordStrength v-if="type === 'password' && showStrength && inputValue" :password="inputValue" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { IconEye, IconEyeOff, IconAlertCircle } from '@/components/icons'
import PasswordStrength from './PasswordStrength.vue'
import type { ValidationResult } from '@/utils/validation'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'text',
    validator: (value: string) => ['text', 'password', 'email', 'number', 'tel', 'url'].includes(value)
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  required: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  validate: {
    type: Function as () => (value: string) => ValidationResult,
    default: null
  },
  showStrength: {
    type: Boolean,
    default: false
  },
  debounce: {
    type: Number,
    default: 300
  }
})

const emit = defineEmits(['update:modelValue', 'error', 'valid'])

const inputValue = ref(props.modelValue)
const error = ref('')
const showPassword = ref(false)

const inputType = computed(() => {
  if (props.type === 'password' && !showPassword.value) {
    return 'password'
  }
  return props.type === 'password' ? 'text' : props.type
})

let debounceTimer: any = null

const validateInput = () => {
  if (props.validate) {
    const result = props.validate(inputValue.value)
    if (!result.valid) {
      error.value = result.message || ''
      emit('error', result.message)
    } else {
      error.value = ''
      emit('valid')
    }
  }
}

const handleInput = () => {
  emit('update:modelValue', inputValue.value)
  
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  
  debounceTimer = setTimeout(() => {
    validateInput()
  }, props.debounce)
}

const handleBlur = () => {
  validateInput()
}

watch(() => props.modelValue, (newVal) => {
  if (newVal !== inputValue.value) {
    inputValue.value = newVal
  }
})

// 暴露验证方法给父组件
const clearError = () => {
  error.value = ''
}

const forceValidate = () => {
  validateInput()
  return !error.value
}

defineExpose({
  clearError,
  forceValidate
})
</script>

<style scoped>
.form-input-wrapper {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.required {
  color: #ff4d4f;
  margin-left: 4px;
}

.form-input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.form-input-container.has-error {
  border-radius: 8px;
  box-shadow: 0 0 0 2px rgba(255, 77, 79, 0.2);
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #d9d9d9;
  border-radius: 8px;
  font-size: 14px;
  color: #303133;
  background: white;
  transition: all 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(13, 148, 136, 0.2);
}

.form-input.has-error {
  border-color: #ff4d4f;
}

.form-input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.toggle-password {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #909399;
}

.toggle-password:hover {
  color: #606266;
}

.toggle-icon {
  width: 18px;
  height: 18px;
}

.error-icon {
  position: absolute;
  right: 12px;
  width: 18px;
  height: 18px;
  color: #ff4d4f;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 6px;
  font-size: 12px;
  color: #ff4d4f;
}

.error-icon-small {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}

/* 淡入淡出动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
