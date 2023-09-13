<script setup lang="ts">
defineProps<{
    fullname: string,
    username: string,
    body: string,
    profilePic: string,
    createdAt: string
}>()
</script>

<template>
    <section
        class="px-4 py-2 grid grid-cols-4 grid-rows-3 gap-x-4 bg-sky-600/10 backdrop-blur-lg border border-solid border-sky-800 rounded-xl">
        <div
            class="col-start-1 col-span-1 row-start-1 row-span-2 flex justify-center items-center border-r border-solid border-sky-600/20">
            <img :src="profilePic" class="w-10 h-10 border border-solid border-sky-800 rounded-full" loading="lazy" />
        </div>
        <div
            class="col-start-1 col-span-1 row-start-3 row-span-1 flex flex-col items-center border-r border-solid border-sky-600/20">
            <span class=" text-sky-600 font-semibold">{{ fullname }}</span>
            <span class="text-sm text-sky-800">{{ username }}</span>
        </div>
        <div class="col-start-2 col-span-3 row-start-1 row-span-1 text-xs text-sky-900">
            {{ new Date(createdAt).toLocaleString() }}
        </div>
        <div class="col-start-2 col-span-3 row-start-2 row-span-2 text-white">
            {{ body }}
        </div>
    </section>
</template>

<style scoped></style>