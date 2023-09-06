<script setup lang="ts">
const { title } = defineProps<{ title: string }>()
</script>

<template>
    <div class="sticky top-0 flex items-center w-fit p-4 text-2xl text-white font-bold capitalize z-20">
        {{ title }}
    </div>
</template>

<style scoped></style>