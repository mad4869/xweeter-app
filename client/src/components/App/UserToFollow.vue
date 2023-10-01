<script setup lang="ts">
defineProps<{
    id: number,
    fullname: string,
    username: string,
    lastXweet: string,
    profilePic: string
}>()
</script>

<template>
    <section class="flex flex-col items-center gap-1 px-8 py-1">
        <router-link :to="`/users/${id}`" 
            class="grid grid-cols-4 grid-rows-2 w-full"
            :title="`View @${username}'s profile`">
            <div class="col-start-1 col-span-1 row-start-1 row-span-2 flex items-center">
                <img 
                    :src="profilePic" 
                    alt="Profile Pic"
                    class="w-8 h-8 border border-solid border-sky-800 rounded-full object-cover" 
                    loading="lazy">
            </div>
            <div class="col-start-2 col-span-3 row-start-1 row-span-1 text-sm text-sky-600 font-bold">
                {{ fullname }}
            </div>
            <div class="col-start-2 col-span-3 row-start-2 row-span-1 text-sm text-sky-600">
                @{{ username }}
            </div>
        </router-link>
        <div 
            class="flex flex-col justify-center gap-1 w-full px-2 py-1 text-xs bg-white/5 rounded-sm">
            <span class="bg-slate-800 w-fit px-1 py text-slate-600 rounded">Last Xweet</span>
            <p class="px-1 text-white italic">{{ lastXweet }}</p>
        </div>
    </section>
</template>