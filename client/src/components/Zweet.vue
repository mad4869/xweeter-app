<script setup lang="ts">
const { username, zweet } = defineProps<{
    username: string,
    zweet: string
}>()
</script>

<template>
    <section
        class="w-3/5 mx-auto mt-4 px-4 py-2 grid grid-cols-4 grid-rows-3 gap-x-4 bg-sky-600/10 backdrop-blur-lg border border-solid border-sky-800 rounded-xl">
        <div class="col-start-1 col-span-1 row-start-1 row-span-2 flex justify-center border-r border-solid border-sky-800">
            <span class="w-10 h-10 px-2 py-2 bg-white border border-solid border-sky-800 rounded-full text-center">A</span>
        </div>
        <div
            class="col-start-1 col-span-1 row-start-3 row-span-1 flex flex-col items-center font-semibold text-sky-800 border-r border-solid border-sky-800">
            {{ username }}
        </div>
        <div class="col-start-2 col-span-3 row-start-1 row-span-1 text-xs text-sky-900">
            {{ new Date().toLocaleTimeString() }}
        </div>
        <div class="col-start-2 col-span-3 row-start-2 row-span-2 text-white">
            {{ zweet }}
        </div>
    </section>
</template>

<style scoped></style>