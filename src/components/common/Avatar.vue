<template>
  <div class="avatar-wrapper">
    <img v-if="avatar" :src="avatar" :alt="name" class="avatar-img" />
    <div v-else class="avatar-text">
      {{ initial }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  avatar?: string
  name?: string
  size?: number
}

const props = withDefaults(defineProps<Props>(), {
  avatar: '',
  name: '',
  size: 48
})

const initial = computed(() => {
  if (!props.name) return 'U'
  return props.name.charAt(0).toUpperCase()
})
</script>

<style scoped>
.avatar-wrapper {
  width: v-bind('size + "px"');
  height: v-bind('size + "px"');
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-tertiary);
  border: 2px solid var(--border-light);
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-text {
  font-size: v-bind('(size / 2.2) + "px"');
  font-weight: 600;
  color: var(--primary-color);
  user-select: none;
}
</style>
