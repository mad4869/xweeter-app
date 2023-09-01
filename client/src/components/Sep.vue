<script setup lang="ts">
const { title } = defineProps<{ title: string }>()
</script>

<template>
    <div class="sticky top-16 flex items-center p-4 bg-slate-900 text-2xl text-white font-bold capitalize z-[5]">
        {{ title }}
    </div>
</template>

<style scoped></style>