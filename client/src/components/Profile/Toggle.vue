<script setup lang="ts">
import { Tabs } from '@/components/Profile/Content.vue';

defineProps<{
    activeTab: Tabs
}>()
defineEmits<{
    (e: 'set-active-tab', tab: Tabs): void
}>()
</script>

<template>
    <div class="flex items-center justify-around py-2 text-xs bg-slate-900 text-slate-600 sticky top-16 z-10">
        <button v-for="tab in Tabs" 
            :key="tab" 
            :class="activeTab === tab ? 'active' : ''"
            class="px-4 py-1 capitalize rounded-full" @click="$emit('set-active-tab', tab)">
            {{ tab }}
        </button>
    </div>
</template>

<style scoped>
.active {
    @apply bg-sky-600 text-white font-semibold transition-colors
}
</style>