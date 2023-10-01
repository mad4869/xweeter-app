<script setup lang="ts">
defineProps<{
    msg: string,
    submsg?: string
}>()
</script>

<template>
    <section
        class="px-4 py-4 flex flex-col justify-center items-center gap-2 bg-sky-600/10 backdrop-blur-lg text-sky-600 border border-solid border-sky-800 rounded-xl">
        <h3 class="text-xl font-bold">{{ msg }}</h3>
        <h6>{{ submsg }}</h6>
    </section>
</template>