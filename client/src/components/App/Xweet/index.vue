<script setup lang="ts">
import { computed, ref } from 'vue';
import { RouterLink } from 'vue-router';

import ImageViewer from './ImageViewer.vue';
import EditXweet from './EditXweet.vue';
import useAuthStore from '@/stores/useAuthStore';
import { sendReqCookie } from '@/utils/axiosInstances';
import { RexweetResponse } from '@/types/rexweets';
import { LikeResponse } from '@/types/likes'
import useRenderXweet from '@/composables/useRenderXweet';
import { XweetResponse } from '@/types/xweets';
import { UpdateTimeline } from '@/types/timeline';
import useCountReplies from '@/composables/useCountReplies';

const { id, body, media, userId, createdAt, updatedAt, rexweeted, liked } = defineProps<{
    id: number,
    userId: number,
    fullname?: string,
    username?: string,
    body: string,
    media?: string,
    profilePic?: string,
    createdAt: string,
    updatedAt?: string,
    og_username?: string,
    og_fullname?: string,
    og_profile_pic?: string,
    isRexweet: boolean,
    isReply: boolean,
    isOwn: boolean,
    rexweeted: boolean,
    liked: boolean
}>()

const emit = defineEmits<{
    (e: 'update-timeline', event: UpdateTimeline, xweet_id?: number): void,
    (e: 'show-notice', category: 'success' | 'error'): void,
    (e: 'reply', xweet_id: number | null): void
}>()

const authStore = useAuthStore()

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
const isEditable = ref(false)
const isRepliable = ref(false)

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
            `/api/xweets/${id}/rexweets`, { userId }
        )

        if (data?.success) {
            console.log('Success!')
        }
    } catch (err) {
        isRexweeted.value = false

        console.error(err)
    }
}

const switchEditable = () => {
    isEditable.value = !isEditable.value
}

const switchRepliable = () => {
    isRepliable.value = !isRepliable.value
    
    if (isRepliable.value) {
        emit('reply', id)
    } else {
        emit('reply', null)
    }
}

const like = async () => {
    isLiked.value = true

    try {
        const { data } = await sendReqCookie.post<LikeResponse | undefined>(
            `/api/xweets/${id}/likes`, { userId }
        )

        if (data?.success) {
            console.log('Success!')
        }
    } catch (err) {
        isLiked.value = false

        console.error(err)
    }
}

const xweet = ref(body)
const xweetText = computed(() => useRenderXweet(xweet.value))
const xweetMedia = ref(media)
const updatedDate = ref(updatedAt)
const repliesCount = ref(await useCountReplies(id))

const handleUpdateXweet = (newBody: string, newMedia?: string, updateDate?: string) => {
    xweet.value = newBody
    xweetMedia.value = newMedia
    updatedDate.value = updateDate
    isEditable.value = false
}

const deleteXweet = async () => {
    emit('update-timeline', UpdateTimeline.Delete, id)

    try {
        const { data } = await sendReqCookie.delete<XweetResponse | undefined>(
            `/api/users/${authStore.getSignedInUserId}/xweets/${id}`
        )

        if (data?.success) {
            emit('show-notice', 'success')
        } else {
            emit('show-notice', 'error')
        }
    } catch (err) {
        emit('update-timeline', UpdateTimeline.Restore)
        emit('show-notice', 'error')

        console.error(err)
    }
}
</script>

<template>
    <section
        class="px-4 py-4 flex justify-center items-center gap-4 bg-sky-600/10 backdrop-blur-lg border border-solid border-sky-800 rounded-xl">
        <router-link
            :to="`/users/${userId}`"
            class="flex-1 flex flex-col items-center gap-2 h-full px-4 border-r border-solid border-sky-600/20">
            <img 
                :src="!isRexweet ? profilePic : og_profile_pic"
                class="w-10 h-10 border border-solid border-sky-800 rounded-full object-cover" 
                loading="lazy" />
            <div class="flex flex-col justify-center items-center text-center">
                <p class=" text-sky-600 font-semibold">{{ !isRexweet ? fullname : og_fullname }}</p>
                <p class="text-sm text-sky-800">@{{ !isRexweet ? username : og_username }}</p>
            </div>
        </router-link>
        <div class="flex flex-col gap-2 w-4/5 h-full">
            <div 
                class="flex justify-between items-center text-xs text-sky-900">
                <p class="flex items-center gap-1">
                    <span class="cursor-help" :title="createdAt">{{ xweetAge }}</span>
                    <em v-if="updatedDate">- Updated at {{ updatedDate }}</em>
                </p>
                <span class="flex justify-center items-center gap-4 text-sm">
                    <span v-if="authStore.getIsAuthenticated && !isReply" class="flex items-center gap-1">
                        <font-awesome-icon
                            v-if="!isRepliable"
                            icon="fa-regular fa-comment"
                            class="transition-transform cursor-pointer hover:text-sky-600 hover:scale-105"
                            title="Reply to this xweet"
                            @click="switchRepliable" />
                        <font-awesome-icon
                            v-else
                            icon="fa-solid fa-comment"
                            class="transition-transform cursor-pointer text-sky-600 scale-105"
                            title="Cancel reply"
                            @click="switchRepliable" />
                        <router-link 
                            :to="`/xweets/${id}`" 
                            v-if="repliesCount" 
                            class="text-xs text-sky-600" 
                            title="View replies">
                            {{ repliesCount }}
                        </router-link>
                    </span>
                    <font-awesome-icon 
                        v-if="authStore.getIsAuthenticated && !isOwn && !isReply"
                        icon="fa-solid fa-retweet" 
                        class="transition-transform cursor-pointer hover:text-sky-600 hover:scale-105"
                        :class="isRexweeted ? 'text-sky-600 scale-105' : ''"
                        title="Rexweet"
                        @click="rexweet" />
                    <font-awesome-icon 
                        v-if="authStore.getIsAuthenticated && !isLiked && !isReply"
                        icon="fa-regular fa-heart"
                        class="transition-transform cursor-pointer hover:text-sky-600 hover:scale-105"
                        title="Like this xweet"
                        @click="like" />
                    <font-awesome-icon
                        v-if="authStore.getIsAuthenticated && isLiked && !isReply"
                        icon="fa-solid fa-heart"
                        class="cursor-pointer text-sky-600 scale-105"
                        title="Unlike this xweet" />
                    <font-awesome-icon
                        v-if="authStore.getIsAuthenticated && isOwn && !isEditable"
                        icon="fa-regular fa-pen-to-square"
                        class="transition-transform cursor-pointer hover:text-sky-600 hover:scale-105"
                        title="Edit this xweet"
                        @click.prevent="switchEditable"
                        />
                    <font-awesome-icon
                        v-if="authStore.getIsAuthenticated && isOwn && isEditable"
                        icon="fa-solid fa-pen-to-square"
                        class="cursor-pointer text-sky-600 scale-105"
                        title="Cancel edit"
                        @click.prevent="switchEditable" />
                    <font-awesome-icon
                        v-if="authStore.getIsAuthenticated && isOwn"
                        icon="fa-regular fa-trash-can"
                        class="transition-transform cursor-pointer hover:text-red-600 hover:scale-105"
                        title="Delete this xweet"
                        @click.prevent="deleteXweet"
                        />
                </span>
            </div>
            <div 
                class="text-sky-800 dark:text-white"
                :class="xweetMedia ? 'row-start-3 row-span-6' : 'row-start-3 row-span-2'">
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
                                class="max-h-60 rounded-md cursor-zoom-in" 
                                loading="lazy"
                                @click="enlargeImage">
                        </div>
                    </div>
                    <EditXweet
                        v-else
                        :key="id"
                        :xweet_id="id" 
                        :body="xweet" 
                        :file-url="xweetMedia" 
                        @update-xweet="handleUpdateXweet" />
                </Transition>
            </div>
            <div></div>
        </div>
    </section>
    <ImageViewer 
        v-if="isImageEnlarged" 
        :username="username!"
        :fullname="fullname!"
        :body="body"
        :profile-pic="profilePic!"
        :file-url="xweetMedia!" 
        :is-own="isOwn"
        :is-liked="isLiked"
        @clicked-outside="handleClickOutside"
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