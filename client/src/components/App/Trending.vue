<script setup lang="ts">
import { sendReqWoCookie } from '../../utils/axiosInstances';
import Hashtag from './Hashtag.vue';
import { HashtagResponse } from '../../types/hashtags'

const getTrending = async (): Promise<HashtagResponse | undefined> => {
    try {
        const { data } = await sendReqWoCookie.get('/api/hashtags')
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
        class="flex-1 flex flex-col gap-4 border border-solid border-sky-800 rounded-xl overflow-hidden">
        <div class="flex justify-between items-center px-4 py-2 bg-sky-600">
            <span class="text-white font-semibold">Trending</span>
            <font-awesome-icon icon="fa-solid fa-globe" class="text-white" />
        </div>
        <div class="overflow-scroll">
            <Hashtag 
                v-for="hashtag in data" 
                :key="hashtag.hashtag_id" 
                :body="hashtag.body" />
        </div>
    </section>
</template>