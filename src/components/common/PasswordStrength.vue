<template>
  <div class="password-strength">
    <div class="strength-bars">
      <div 
        v-for="i in 5" 
        :key="i" 
        class="strength-bar"
        :class="{ 
          active: i <= strength.level,
          weak: strength.level > 0 && strength.level <= 2,
          medium: strength.level > 2 && strength.level <= 4,
          strong: strength.level > 4
        }"
      ></div>
    </div>
    <div class="strength-text" :style="{ color: strength.color }">
      {{ strength.text }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { getPasswordStrength } from '@/utils/validation'

const props = defineProps({
  password: {
    type: String,
    default: ''
  }
})

const strength = computed(() => getPasswordStrength(props.password))
</script>

<style scoped>
.password-strength {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 8px;
}

.strength-bars {
  display: flex;
  gap: 4px;
  flex: 1;
}

.strength-bar {
  height: 4px;
  flex: 1;
  border-radius: 2px;
  background: #f0f0f0;
  transition: all 0.3s ease;
}

.strength-bar.active.weak {
  background: #ff4d4f;
}

.strength-bar.active.medium {
  background: #faad14;
}

.strength-bar.active.strong {
  background: #52c41a;
}

.strength-text {
  font-size: 12px;
  font-weight: 500;
  min-width: 32px;
  text-align: right;
}
</style>
