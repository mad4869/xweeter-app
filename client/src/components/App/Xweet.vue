<script setup lang="ts">
defineProps<{
    fullname?: string,
    username?: string,
    body: string,
    media?: string,
    profilePic?: string,
    createdAt: string,
    isRexweet: boolean,
    og_username?: string,
    og_fullname?: string,
    og_profile_pic?: string
}>()
</script>

<template>
    <section
        class="px-4 py-2 grid grid-cols-4 gap-x-4 bg-sky-600/10 backdrop-blur-lg border border-solid border-sky-800 rounded-xl"
        :class="media ? 'grid-rows-[8]' : 'grid-rows-3'">
        <div
            class="col-start-1 col-span-1 flex justify-center items-center border-r border-solid border-sky-600/20"
            :class="media ? 'row-start-1 row-span-4' : 'row-start-1 row-span-2'">
            <img 
                :src="!isRexweet ? profilePic : og_profile_pic"
                class="w-10 h-10 border border-solid border-sky-800 rounded-full" 
                loading="lazy" />
        </div>
        <div
            class="col-start-1 col-span-1 flex flex-col items-center border-r border-solid border-sky-600/20"
            :class="media ? 'row-start-5 row-span-3' : 'row-start-3 row-span-1'">
            <span class=" text-sky-600 font-semibold">{{ !isRexweet ? fullname : og_fullname }}</span>
            <span class="text-sm text-sky-800">@{{ !isRexweet ? username : og_username }}</span>
        </div>
        <div 
            class="col-start-2 col-span-3 row-start-1 row-span-1 flex justify-between items-center text-xs text-sky-900">
            <span>{{ new Date(createdAt).toLocaleString() }}</span>
            <span class="flex justify-center items-center gap-2">
                <font-awesome-icon 
                    icon="fa-solid fa-retweet" 
                    class="text-sm transition-transform cursor-pointer hover:text-sky-600 hover:scale-105"
                    title="Rexweet" />
                <font-awesome-icon 
                    icon="fa-regular fa-heart"
                    class="text-sm transition-transform cursor-pointer hover:text-sky-600 hover:scale-105"
                    title="Like" />
            </span>
        </div>
        <div 
            class="col-start-2 col-span-3 flex flex-col gap-2 text-sky-800 dark:text-white"
            :class="media ? 'row-start-3 row-span-5' : 'row-start-2 row-span-2'">
            <p>{{ body }}</p>
            <div class="flex-shrink-0">
                <img 
                    :src="media" 
                    class="max-h-40 cursor-zoom-in" 
                    alt="Media" 
                    loading="lazy"
                    v-if="media">
            </div>
        </div>
    </section>
</template>