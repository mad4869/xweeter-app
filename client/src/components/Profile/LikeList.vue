<script setup lang="ts">
import { ref, reactive, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useScroll } from '@vueuse/core';

import Xweet from '@/components/App/Xweet/index.vue';
import ReplyXweet from '@/components/App/Xweet/ReplyXweet.vue';
import MoreXweet from '@/components/App/Xweet/MoreXweet.vue';
import Empty from '@/components/App/Empty.vue';
import useAuthStore from '@/stores/useAuthStore';
import { ProfileTimelineResponse, UpdateTimeline } from '@/types/timeline';
import { LikeDetailResponse } from '@/types/likes'
import { RexweetDetailResponse } from '@/types/rexweets'
import { sendReqCookie, sendReqWoCookie } from '@/utils/axiosInstances';

defineProps<{
    y: number
    showNotice: (category: 'success' | 'error', msg: string) => void
}>()
const emit = defineEmits<{
    (e: 'show-notice', category: 'success' | 'error', msg: string): void
}>()

const authStore = useAuthStore()

const route = useRoute()

const start = ref(0)
const getLikes = async () => {
    try {
        const { data } = await sendReqWoCookie.get<ProfileTimelineResponse | undefined>(
            `/api/users/${route.params.id}/likes?start=${start.value}`
        )
        if (data?.success) {
            return data.data
        }
    } catch (err) {
        console.error(err)
    }
}

const initialLikes = await getLikes() || []
const likes = reactive(initialLikes)

const updateTimeline = (event: UpdateTimeline, xweet_id?: number | null) => {
    if (event === UpdateTimeline.Delete) {
        const index = likes.findIndex(xweet => xweet.xweet_id === xweet_id)
        if (index !== -1) {
            likes.splice(index, 1)
        }
    }

    if (event === UpdateTimeline.Restore) {
        likes.length = 0
        likes.push(...initialLikes)
    }
}

const getLikesRexweets = async () => {
    try {
        if (authStore.getIsAuthenticated) {
            const likes = await sendReqCookie.get<LikeDetailResponse | undefined>(
                `/api/users/${authStore.getSignedInUserId}/likes`
            )
            const rexweets = await sendReqCookie.get<RexweetDetailResponse | undefined>(
                `/api/users/${authStore.getSignedInUserId}/rexweets`
            )
            if (likes.data && rexweets.data) {
                const likesData = likes.data
                const rexweetsData = rexweets.data

                return {
                    likesData: likesData.data,
                    rexweetsData: rexweetsData.data
                }
            }
        }
    } catch (err) {
        console.error(err)
    }
}

const signedInUserLikes = reactive<number[]>([])
const signedInUserRexweets = reactive<number[]>([])
const { likesData, rexweetsData } = (await getLikesRexweets()) || { data: [] }
likesData?.forEach(like => {
    signedInUserLikes.push(like.xweet_id)
})
rexweetsData?.forEach(rexweet => {
    signedInUserRexweets.push(rexweet.xweet_id)
})

const xweetToReply = ref<number | null>()
const xweetToDelete = ref<number | null>()
const showModal = ref(false)
const isLoading = ref(false)

const likeRef = ref<HTMLElement | null>(null)
const { arrivedState } = useScroll(likeRef)
const needMoreXweet = ref(true)
if (likes.length <= 4) {
    needMoreXweet.value = false
}

watch(() => arrivedState.bottom, async () => {
    if (needMoreXweet) {
        start.value+= 10
        isLoading.value = true
    
        const newLikes = await getLikes() || []
        isLoading.value = false
    
        if (newLikes.length === 0) {
            needMoreXweet.value = false
        } else {
            likes.push(...newLikes)
        }
    }
})
</script>

<template>
    <section class="flex flex-col max-h-screen gap-4 overflow-y-scroll scrollbar-hide" ref="likeRef">
        <div v-for="xweet in likes">
            <Xweet
                :key="xweet.xweet_id" 
                :id="xweet.xweet_id" 
                :userId="xweet.user_id"
                :fullname="xweet.full_name" 
                :username="xweet.username" 
                :body="xweet.body" 
                :media="xweet.media"
                :profilePic="xweet.profile_pic" 
                :createdAt="xweet.created_at" 
                :updated-at="xweet.updated_at"
                :og-user-id="xweet.og_user_id"
                :og-fullname="xweet.og_full_name"
                :og-username="xweet.og_username"
                :og-profile-pic="xweet.og_profile_pic" 
                :is-rexweet="xweet.rexweet_id !== undefined"
                :is-own="xweet.user_id === authStore.getSignedInUserId" 
                :rexweeted="signedInUserRexweets.includes(xweet.xweet_id)"
                :liked="signedInUserLikes.includes(xweet.xweet_id)"
                @update-timeline="updateTimeline"
                @show-notice="showNotice"
                @reply="(xweetId) => { xweetToReply = xweetId }"
                @delete="(xweetId) => { showModal = true; xweetToDelete = xweetId }" />
            <ReplyXweet 
                :show="xweetToReply === xweet.xweet_id"
                :xweet-id="xweet.xweet_id"
                @close-reply="() => { xweetToReply = null }" />
        </div>
        <MoreXweet v-if="needMoreXweet" :is-loading="isLoading" />
        <Empty 
            v-if="likes.length === 0"
            msg="There are no likes yet" />
    </section>
</template>