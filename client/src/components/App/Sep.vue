<script setup lang="ts">
defineProps<{ 
    isSticky: boolean, 
    title: string, 
    subtitle?: string 
}>()
</script>

<template>
    <div 
        class="flex items-center w-fit p-4 text-2xl text-sky-800 dark:text-white"
        :class="isSticky ? 'sticky top-0 z-20' : ''">
        <h1><strong>{{ title }}</strong> <span>{{ subtitle }}</span></h1>
    </div>
</template>