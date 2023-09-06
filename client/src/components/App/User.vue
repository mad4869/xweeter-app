<script setup lang="ts">
const { fullname, username, lastZweet } = defineProps<{
    fullname: string,
    username: string,
    lastZweet: string
}>()
</script>

<template>
    <section class="flex flex-col items-center gap-1 px-2 py-1">
        <div class="grid grid-cols-4 grid-rows-2 w-full">
            <div class="col-start-1 col-span-1 row-start-1 row-span-2 flex justify-center items-center">
                <span
                    class="w-6 h-6 px-1 py-1 bg-white border border-solid border-sky-800 rounded-full text-xs text-center">A</span>
            </div>
            <div class="col-start-2 col-span-3 row-start-1 row-span-1 text-sm text-sky-600 font-bold">
                {{ fullname }}
            </div>
            <div class="col-start-2 col-span-3 row-start-2 row-span-1 text-sm text-sky-600">
                {{ username }}
            </div>
        </div>
        <div class="flex flex-col justify-center w-full px-3 pb-2 border-b border-solid border-sky-800">
            <span class="w-fit bg-slate-600 px-2 text-xs text-white rounded-full">Last zweet</span>
            <p class=" text-white italic">{{ lastZweet }}</p>
        </div>
    </section>
</template>

<style scoped></style>