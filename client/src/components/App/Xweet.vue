<script setup lang="ts">
import { ref } from 'vue';
import { RouterLink } from 'vue-router';

import ImageViewer from './ImageViewer.vue';
import useAuth from '../../composables/useAuth';
import { sendReqCookie } from '../../utils/axiosInstances';
import { RexweetResponse } from '../../types/rexweets';
import { LikeResponse } from '../../types/likes'
import useRenderXweet from '../../composables/useRenderXweet';

const { id, body, user_id, createdAt, rexweeted, liked } = defineProps<{
    id: number,
    user_id: number,
    fullname?: string,
    username?: string,
    body: string,
    media?: string,
    profilePic?: string,
    createdAt: string,
    og_username?: string,
    og_fullname?: string,
    og_profile_pic?: string,
    isRexweet: boolean,
    isOwn: boolean,
    rexweeted: boolean,
    liked: boolean
}>()

const authStore = useAuth()

const currentDate = new Date()
const xweetDate = new Date(createdAt)
const deltaDate = currentDate.getTime() - xweetDate.getTime()

const seconds = Math.floor(deltaDate / 1000)
const minutes = Math.floor(seconds / 60)
const hours = Math.floor(minutes / 60)
const days = Math.floor(hours / 24)
const months = Math.floor(days / 30)
const years = Math.floor(months / 12)

const xweetAge = ref('')

switch(true) {
    case years > 0:
        xweetAge.value = `${years} year${years !== 1 ? 's' : ''} ago`
        break
    case months > 0:
        xweetAge.value = `${months} month${months !== 1 ? 's' : ''} ago`
        break
    case days > 0:
        xweetAge.value = `${days} day${days !== 1 ? 's' : ''} ago`
        break
    case hours > 0:
        xweetAge.value = `${hours} hour${hours !== 1 ? 's' : ''} ago`;
        break;
    case minutes > 0:
        xweetAge.value = `${minutes} minute${minutes !== 1 ? 's' : ''} ago`;
        break;
    default:
        xweetAge.value = `${seconds} second${seconds !== 1 ? 's' : ''} ago`;
        break;
}

const isImageEnlarged = ref(false)
const isRexweeted = ref(rexweeted)
const isLiked = ref(liked)

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

const xweet = useRenderXweet(body)
</script>

<template>
    <section
        class="px-4 py-4 flex justify-center items-center gap-4 bg-sky-600/10 backdrop-blur-lg border border-solid border-sky-800 rounded-xl">
        <div
            class="flex-1 flex flex-col items-center gap-2 h-full px-4 border-r border-solid border-sky-600/20">
            <img 
                :src="!isRexweet ? profilePic : og_profile_pic"
                class="w-10 h-10 border border-solid border-sky-800 rounded-full" 
                loading="lazy" />
            <div class="flex flex-col justify-center items-center text-center">
                <p class=" text-sky-600 font-semibold">{{ !isRexweet ? fullname : og_fullname }}</p>
                <p class="text-sm text-sky-800">@{{ !isRexweet ? username : og_username }}</p>
            </div>
        </div>
        <div class="flex flex-col gap-2 w-4/5 h-full">
            <div 
                class="flex justify-between items-center text-xs text-sky-900">
                <span :title="createdAt">{{ xweetAge }}</span>
                <span class="flex justify-center items-center gap-4">
                    <font-awesome-icon 
                        v-if="authStore.getIsAuthenticated && !isOwn"
                        icon="fa-solid fa-retweet" 
                        class="text-sm transition-transform cursor-pointer hover:text-sky-600 hover:scale-105"
                        :class="isRexweeted ? 'text-sky-600 scale-105' : ''"
                        title="Rexweet"
                        @click="rexweet" />
                    <font-awesome-icon 
                        v-if="authStore.getIsAuthenticated && !isLiked"
                        icon="fa-regular fa-heart"
                        class="text-sm transition-transform cursor-pointer hover:text-sky-600 hover:scale-105"
                        title="Like Xweet"
                        @click="like" />
                    <font-awesome-icon
                        v-if="authStore.getIsAuthenticated && isLiked"
                        icon="fa-solid fa-heart"
                        class="text-sm transition-transform cursor-pointer text-sky-600 scale-105"
                        title="Unlike Xweet" />
                    <font-awesome-icon
                        v-if="authStore.getIsAuthenticated && isOwn"
                        icon="fa-regular fa-pen-to-square"
                        class="text-sm transition-transform cursor-pointer hover:text-sky-600 hover:scale-105"
                        title="Edit Xweet"
                        />
                    <font-awesome-icon
                        v-if="authStore.getIsAuthenticated && isOwn"
                        icon="fa-regular fa-trash-can"
                        class="text-sm transition-transform cursor-pointer hover:text-red-600 hover:scale-105"
                        title="Delete Xweet"
                        />
                </span>
            </div>
            <div 
                class="flex flex-col gap-2 text-sky-800 dark:text-white"
                :class="media ? 'row-start-3 row-span-6' : 'row-start-3 row-span-2'">
                <div class="break-words">
                    <template v-for="(word, index) in xweet">
                        <component 
                            :is="word.type" 
                            :to="word.to" 
                            :class="word.type === RouterLink ? 'text-sky-600 hover:text-sky-400' : ''">
                            {{ word.text }}
                        </component>
                        <span v-if="index < xweet.length - 1" v-html="`&nbsp;`" />
                    </template>
                </div>
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
        </div>
    </section>
    <ImageViewer 
        v-if="isImageEnlarged" 
        :username="username!"
        :fullname="fullname!"
        :body="body"
        :profile-pic="profilePic!"
        :file-url="media!" 
        :is-own="isOwn"
        :is-liked="isLiked"
        @clicked-outside="handleClickOutside"
        />
</template>