<script setup lang="ts">
const { title } = defineProps<{ title: string }>()
</script>

<template>
    <div
        class="sticky top-16 flex items-center w-3/5 mx-auto mt-4 p-4 bg-slate-900 text-2xl text-white font-bold capitalize z-[5]">
        {{ title }}
    </div>
</template>

<style scoped></style>