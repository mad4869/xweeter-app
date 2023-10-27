<script setup lang="ts">
import { computed, ref } from 'vue';
import { RouterLink } from 'vue-router';
import { useDateFormat } from '@vueuse/core';

import ImageViewer from './ImageViewer.vue';
import EditXweet from './EditXweet.vue';
import useRenderXweet from '@/composables/useRenderXweet';
import useTimestamp from '@/composables/useTimestamp';
import useAuthStore from '@/stores/useAuthStore';
import { sendReqCookie } from '@/utils/axiosInstances';
import { RexweetResponse } from '@/types/rexweets';
import { LikeResponse } from '@/types/likes'

const { id, username, body, media, userId, createdAt, updatedAt, rexweeted, liked } = defineProps<{
    id: number
    userId: number
    fullname?: string
    username?: string
    body: string
    media?: string
    profilePic?: string
    createdAt: string
    updatedAt?: string
    ogUserId?: number
    ogUsername?: string
    ogFullname?: string
    ogProfilePic?: string
    isRexweet: boolean
    isOwn: boolean
    rexweeted: boolean
    liked: boolean
}>()

const emit = defineEmits<{
    (e: 'show-notice', category: 'success' | 'error', msg: string): void,
    (e: 'reply', xweet_id: number | null): void
    (e: 'delete', xweet_id: number): void
}>()

const authStore = useAuthStore()

const isImageEnlarged = ref(false)
const isRexweeted = ref(rexweeted)
const isLiked = ref(liked)
const isEditable = ref(false)
const isRepliable = ref(false)
const xweet = ref(body)
const xweetText = computed(() => useRenderXweet(xweet.value))
const xweetMedia = ref(media)
const xweetTimestamp = ref(useTimestamp(createdAt))
const xweetUpdatedTimestamp = ref(useTimestamp(updatedAt))
const xweetRepliesCount = ref(0)

const rexweet = async () => {
    isRexweeted.value = true

    try {
        const { data } = await sendReqCookie.post<RexweetResponse | undefined>(
            `/api/xweets/${id}/rexweets`, { userId: authStore.getSignedInUserId }
        )

        if (data?.success) {
            emit('show-notice', 'success', `You rexweeted ${username}'s xweet`)
        }
    } catch (err) {
        isRexweeted.value = false

        emit('show-notice', 'error', 'Failed to rexweet: error occured during the process')

        console.error(err)
    }
}

const switchRepliable = () => {
    isRepliable.value = !isRepliable.value
    
    if (isRepliable.value) {
        emit('reply', id)
    } else {
        emit('reply', null)
    }
}

const likeXweet = async () => {
    isLiked.value = true

    try {
        const { data } = await sendReqCookie.post<LikeResponse | undefined>(
            `/api/xweets/${id}/likes`, { userId: authStore.getSignedInUserId }
        )

        if (data?.success) {
            emit('show-notice', 'success', `You liked ${username}'s xweet`)
        }
    } catch (err) {
        isLiked.value = false

        emit('show-notice', 'error', 'Failed to like xweet: error occured during the process')

        console.error(err)
    }
}

const updateXweet = (newBody: string, newMedia?: string, updateDate?: string) => {
    xweet.value = newBody
    xweetMedia.value = newMedia
    xweetUpdatedTimestamp.value = useTimestamp(updateDate)
    isEditable.value = false
}
</script>

<template>
    <section
        class="flex justify-center gap-4 px-4 py-4 border border-solid bg-sky-600/10 backdrop-blur-lg border-sky-800 rounded-xl">
        <router-link
            :to="`/users/${!isRexweet ? userId : ogUserId}`"
            class="flex-1 flex flex-col items-center gap-2 px-4 border-r border-solid border-sky-600/20">
            <img 
                :src="!isRexweet ? profilePic : ogProfilePic"
                class="object-cover w-10 h-10 border border-solid rounded-full border-sky-800" 
                loading="lazy" />
            <div class="flex flex-col items-center justify-center text-center">
                <p class="font-semibold text-sky-600">{{ !isRexweet ? fullname : ogFullname }}</p>
                <p class="text-sm text-sky-800 break-all">@{{ !isRexweet ? username : ogUsername }}</p>
            </div>
        </router-link>
        <div class="flex flex-col w-4/5 h-full gap-2">
            <div 
                class="flex items-center justify-between text-xs text-sky-900">
                <p class="flex items-center gap-1">
                    <span class="cursor-help" :title="useDateFormat(createdAt, 'D-M-YYYY HH:mm').value">
                        {{ xweetTimestamp }}
                    </span>
                    <em 
                        v-if="xweetUpdatedTimestamp" 
                        class="cursor-help" 
                        :title="useDateFormat(updatedAt, 'D-M-YYYY HH:mm').value">
                        - Updated {{ xweetUpdatedTimestamp }}
                    </em>
                </p>
                <span class="flex items-center justify-center gap-4 text-sm">
                    <span v-if="authStore.getIsAuthenticated" class="flex items-center gap-1">
                        <font-awesome-icon
                            v-if="!isRepliable"
                            icon="fa-regular fa-comment"
                            class="transition-transform cursor-pointer hover:text-sky-600 hover:scale-105"
                            title="Reply to this xweet"
                            @click="switchRepliable" />
                        <font-awesome-icon
                            v-else
                            icon="fa-solid fa-comment"
                            class="transition-transform scale-105 cursor-pointer text-sky-600"
                            title="Cancel reply"
                            @click="switchRepliable" />
                        <router-link 
                            :to="`/xweets/${id}`"
                            v-if="xweetRepliesCount"  
                            class="text-xs text-sky-600" 
                            title="View replies">
                            {{ xweetRepliesCount }}
                        </router-link>
                    </span>
                    <font-awesome-icon 
                        v-if="authStore.getIsAuthenticated && !isOwn"
                        icon="fa-solid fa-retweet" 
                        class="transition-transform cursor-pointer hover:text-sky-600 hover:scale-105"
                        :class="isRexweeted ? 'text-sky-600 scale-105' : ''"
                        title="Rexweet"
                        @click="rexweet" />
                    <font-awesome-icon 
                        v-if="authStore.getIsAuthenticated && !isLiked"
                        icon="fa-regular fa-heart"
                        class="transition-transform cursor-pointer hover:text-sky-600 hover:scale-105"
                        title="Like this xweet"
                        @click="likeXweet" />
                    <font-awesome-icon
                        v-if="authStore.getIsAuthenticated && isLiked"
                        icon="fa-solid fa-heart"
                        class="scale-105 cursor-pointer text-sky-600"
                        title="Unlike this xweet" />
                    <font-awesome-icon
                        v-if="authStore.getIsAuthenticated && isOwn && !isEditable"
                        icon="fa-regular fa-pen-to-square"
                        class="transition-transform cursor-pointer hover:text-sky-600 hover:scale-105"
                        title="Edit this xweet"
                        @click="() => { isEditable = true }"
                        />
                    <font-awesome-icon
                        v-if="authStore.getIsAuthenticated && isOwn && isEditable"
                        icon="fa-solid fa-pen-to-square"
                        class="scale-105 cursor-pointer text-sky-600"
                        title="Cancel edit"
                        @click="() => { isEditable = false }" />
                    <font-awesome-icon
                        v-if="authStore.getIsAuthenticated && isOwn"
                        icon="fa-regular fa-trash-can"
                        class="transition-transform cursor-pointer hover:text-red-600 hover:scale-105"
                        title="Delete this xweet"
                        @click="$emit('delete', id)"
                        />
                </span>
            </div>
            <div 
                class="text-sky-800 dark:text-white">
                <Transition mode="out-in">
                    <div v-if="!isEditable" class="flex flex-col gap-2">
                        <router-link :to="`/xweets/${id}`" class="break-words">
                            <template v-for="(word, index) in xweetText">
                                <component 
                                    :is="word.type" 
                                    :to="word.to"
                                    :title="word.type === RouterLink ? `View ${word.text}` : ''" 
                                    :class="word.type === RouterLink ? 'text-sky-600 hover:text-sky-400' : ''">
                                    {{ word.text }}
                                </component>
                                <span v-if="index < xweet.length - 1" v-html="`&nbsp;`" />
                            </template>
                        </router-link>
                        <div class="flex-shrink-0">
                            <img 
                                :src="xweetMedia" 
                                v-if="xweetMedia"
                                alt="Media" 
                                class="rounded-md max-h-60 cursor-zoom-in" 
                                loading="lazy"
                                @click="() => { isImageEnlarged = true }">
                        </div>
                    </div>
                    <EditXweet
                        v-else
                        :key="id"
                        :xweet_id="id" 
                        :body="xweet" 
                        :file-url="xweetMedia" 
                        @update-xweet="updateXweet" />
                </Transition>
            </div>
            <div></div>
        </div>
    </section>
    <ImageViewer 
        :show="isImageEnlarged" 
        :username="username!"
        :fullname="fullname!"
        :body="body"
        :profile-pic="profilePic!"
        :file-url="xweetMedia!" 
        :is-own="isOwn"
        :is-liked="isLiked"
        @clicked-outside="() => { isImageEnlarged = false }"
        />
</template>

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.2s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>