<template>
  <SvgIcon viewBox="0 0 24 24">
    <path 
      :d="isFilled 
        ? 'M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z'
        : 'M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z'"
      :fill="isFilled ? 'currentColor' : 'none'"
      stroke="currentColor" 
      stroke-width="2" 
      stroke-linecap="round" 
      stroke-linejoin="round"
    />
  </SvgIcon>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import SvgIcon from './SvgIcon.vue'

const props = defineProps<{
  filled?: boolean
}>()

const isFilled = computed(() => props.filled || false)
</script>
