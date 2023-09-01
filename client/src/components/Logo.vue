<script setup lang="ts">
const props = defineProps<{ size: 'w-8' | 'w-16' | 'w-32' }>()
</script>

<template>
    <img :class="props.size" src="../assets/logo.png" loading="lazy">
</template>

<style scoped></style>