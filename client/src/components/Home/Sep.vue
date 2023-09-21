<script setup lang="ts">
defineProps<{ title: string }>()
</script>

<template>
    <div 
        class="sticky top-0 flex items-center w-fit p-4 text-2xl text-sky-800 font-bold capitalize z-20 dark:text-white">
        {{ title }}
    </div>
</template>