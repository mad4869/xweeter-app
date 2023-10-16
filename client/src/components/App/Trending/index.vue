<script setup lang="ts">
import Hashtag from './Hashtag.vue';
import { sendReqWoCookie } from '@/utils/axiosInstances';
import { TrendingResponse } from '@/types/hashtags'

const getTrending = async (): Promise<TrendingResponse | undefined> => {
    try {
        const { data } = await sendReqWoCookie.get('/api/trending')
        if (data) {
            return data
        }
    } catch (err) {
        console.error(err)
    }
}

const { data } = (await getTrending()) || { data: [] }
</script>

<template>
    <section 
        class="flex flex-col flex-1 gap-4 overflow-hidden border border-solid border-sky-800 rounded-xl">
        <div class="flex items-center justify-between px-4 py-2 bg-sky-600">
            <span class="font-semibold text-white">Trending</span>
            <font-awesome-icon icon="fa-solid fa-globe" class="text-white" />
        </div>
        <div class="overflow-scroll">
            <Hashtag 
                v-for="hashtag in data" 
                :key="hashtag.hashtag_id" 
                :body="hashtag.body"
                :xweet-count="hashtag.xweet_count" />
        </div>
    </section>
</template>