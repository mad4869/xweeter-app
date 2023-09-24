<script setup lang="ts">
import { ref } from 'vue';

import ImageViewer from './ImageViewer.vue';
import useAuth from '../../composables/useAuth';
import { sendReqCookie } from '../../utils/axiosInstances';
import { RexweetResponse } from '../../types/rexweets';
import { LikeResponse } from '../../types/likes'

const { id, user_id } = defineProps<{
    id: number,
    user_id: number,
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

const authStore = useAuth()

const isImageEnlarged = ref(false)
const isRexweeted = ref(false)
const isLiked = ref(false)

const enlargeImage = () => {
    isImageEnlarged.value = true
}

const handleClickOutside = (isClickedOutside: boolean) => {
    if (isClickedOutside) {
        isImageEnlarged.value = false
    }
}

const rexweet = async () => {
    isRexweeted.value = true

    try {
        const { data } = await sendReqCookie.post<RexweetResponse | undefined>(
            `/api/xweets/${id}/rexweets`, { user_id }
        )

        if (data?.success) {
            console.log('Success!')
        }
    } catch (err) {
        isRexweeted.value = false

        console.error(err)
    }
}

const like = async () => {
    isLiked.value = true

    try {
        const { data } = await sendReqCookie.post<LikeResponse | undefined>(
            `/api/xweets/${id}/likes`, { user_id }
        )

        if (data?.success) {
            console.log('Success!')
        }
    } catch (err) {
        isLiked.value = false

        console.error(err)
    }
}
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
                    v-if="authStore.getIsAuthenticated"
                    icon="fa-solid fa-retweet" 
                    class="text-sm transition-transform cursor-pointer hover:text-sky-600 hover:scale-105"
                    :class="isRexweeted ? 'text-sky-600 scale-105' : ''"
                    title="Rexweet"
                    @click="rexweet" />
                <font-awesome-icon 
                    v-if="authStore.getIsAuthenticated && !isLiked"
                    icon="fa-regular fa-heart"
                    class="text-sm transition-transform cursor-pointer hover:text-sky-600 hover:scale-105"
                    title="Like"
                    @click="like" />
                <font-awesome-icon
                    v-if="authStore.getIsAuthenticated && isLiked"
                    icon="fa-solid fa-heart"
                    class="text-sm transition-transform cursor-pointer text-sky-600 scale-105"
                    title="Unlike" />
            </span>
        </div>
        <div 
            class="col-start-2 col-span-3 flex flex-col gap-2 text-sky-800 dark:text-white"
            :class="media ? 'row-start-3 row-span-5' : 'row-start-2 row-span-2'">
            <p>{{ body }}</p>
            <div class="flex-shrink-0">
                <img 
                    :src="media" 
                    v-if="media"
                    alt="Media" 
                    class="max-h-60 cursor-zoom-in" 
                    loading="lazy"
                    @click="enlargeImage">
            </div>
        </div>
    </section>
    <ImageViewer 
        v-if="isImageEnlarged" 
        :username="username!"
        :fullname="fullname!"
        :body="body"
        :profile-pic="profilePic!"
        :file-url="media!" 
        @clicked-outside="handleClickOutside"
        />
</template>