<template>
  <div id="app">
    <transition name="fade" mode="out-in">
      <router-view />
    </transition>
    <Toast />
  </div>
</template>

<script setup lang="ts">
import Toast from './components/common/Toast.vue'
import { createToast } from './composables/useToast'

createToast()
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

#app {
  min-height: 100vh;
}

/* 页面切换过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--transition-normal);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
