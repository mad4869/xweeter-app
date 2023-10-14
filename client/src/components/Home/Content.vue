<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useWindowScroll } from '@vueuse/core';

import Xweet from '@/components/App/Xweet/index.vue';
import NewXweet from '@/components/App/Xweet/NewXweet.vue';
import ReplyXweet from '@/components/App/Xweet/ReplyXweet.vue';
import MoreXweet from '@/components/App/Xweet/MoreXweet.vue';
import Empty from '@/components/App/Empty.vue';
import Sep from '@/components/App/Sep.vue';
import Modal from '@/components/App/Modal.vue';
import useAuthStore from '@/stores/useAuthStore';
import { countStore } from '@/stores/useCountStore'
import { XweetDetail, XweetResponse, XweetsResponse } from '@/types/xweets';
import { UpdateTimeline } from '@/types/timeline';
import { LikeDetailResponse } from '@/types/likes'
import socket from '@/utils/socket';
import { sendReqCookie, sendReqWoCookie } from '@/utils/axiosInstances';

defineProps<{
    showNotice: (category: 'success' | 'error', msg: string) => void
}>()
const emit = defineEmits<{
    (e: 'show-notice', category: 'success' | 'error', msg: string): void
}>()

const authStore = useAuthStore()

const start = ref(0)
const getTimeline = async (): Promise<XweetsResponse | undefined> => {
    try {
        if (authStore.getIsAuthenticated) {
            const { data } = await sendReqCookie.get(
                `/api/users/${authStore.getSignedInUserId}/timeline?start=${start.value}`
            )
            if (data) {
                return data
            }
        } else {
            const { data } = await sendReqWoCookie.get(`/api/timeline`)
            if (data) {
                return data
            }
        }
    } catch (err) {
        console.error(err)
    }
}

const timelineData = (await getTimeline()) || { data: [] }
const initialTimeline = [...timelineData.data]
const timeline = reactive<XweetDetail[]>(initialTimeline)

socket.on('add_to_timeline', (xweet) => {
    timeline.unshift(xweet)
})

const updateTimeline = (event: UpdateTimeline, xweet_id?: number | null) => {
    if (event === UpdateTimeline.Delete) {
        const index = timeline.findIndex(xweet => xweet.xweet_id === xweet_id)
        if (index !== -1) {
            timeline.splice(index, 1)
        }
    }

    if (event === UpdateTimeline.Restore) {
        timeline.length = 0
        timeline.push(...initialTimeline)
    }
}

const getLikes = async (): Promise<LikeDetailResponse | undefined> => {
    try {
        if (authStore.getIsAuthenticated) {
            const { data } = await sendReqCookie.get(`/api/users/${authStore.getSignedInUserId}/likes`)
            if (data) {
                return data
            }
        }
    } catch (err) {
        console.error(err)
    }
}

const likes = reactive<number[]>([])
const likesData = (await getLikes()) || { data: [] }
likesData.data.forEach(like => {
    likes.push(like.xweet_id)
})

const xweetToReply = ref<number | null>()
const xweetToDelete = ref<number | null>()

const moreXweet = ref<HTMLElement | null>(null)
// const needsMoreXweet = ref(true)
const threshold = ref<number | undefined>(0)
const { y } = useWindowScroll()

const moreXweetRect = moreXweet.value?.getBoundingClientRect()
threshold.value = (moreXweetRect?.top || 0)

console.log(threshold.value, y.value)

// watch(y, async (newY, oldY) => {
//     if (newY >= (threshold.value ?? 0) && newY !== oldY) {
//         isLoading.value = true
//         start.value+= 10
        
//         try {
//             const { data } = (await getTimeline()) || { data: [] }
//             if (data.length > 0) {
//                 timeline.push(...data)
//             } else {
//                 needsMoreXweet.value = false
//             }
//         } catch (err) {
//             console.error('Error fetching timeline data:', err);
//         } finally {
//             isLoading.value = false;
//         }
//     }
// })
const showModal = ref(false)
const isLoading = ref(false)
const isError = ref(false)

const deleteXweet = async (xweet_id?: number | null) => {
    isLoading.value = true

    try {
        const { data } = await sendReqCookie.delete<XweetResponse | undefined>(
            `/api/users/${authStore.getSignedInUserId}/xweets/${xweet_id}`
        )

        if (data?.success) {
            isLoading.value = false
            showModal.value = false
            
            updateTimeline(UpdateTimeline.Delete, xweetToDelete.value)
            countStore.decrementXweetsCount()
            emit('show-notice', 'error', 'You have deleted the xweet')
        }
    } catch (err) {
        isError.value = true

        setTimeout(() => {
            isError.value = false
        }, 2000)

        console.error(err)
    }
}
</script>

<template>
    <NewXweet 
        v-if="authStore.getIsAuthenticated" 
        @increment-xweet-count="() => { countStore.incrementXweetsCount() }" />
    <Sep title="Timeline" is-sticky />
    <div v-for="xweet in timeline" class="flex flex-col gap-4">
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
            :is-rexweet="false"
            :is-reply="false"
            :is-own="xweet.user_id === authStore.getSignedInUserId" 
            :rexweeted="false"
            :liked="likes.includes(xweet.xweet_id)"
            @update-timeline="updateTimeline"
            @show-notice="showNotice"
            @reply="(xweetId) => { xweetToReply = xweetId }"
            @delete="(xweetId) => { showModal = true; xweetToDelete = xweetId }" />
        <ReplyXweet 
            :show="xweetToReply === xweet.xweet_id"
            :xweet-id="xweet.xweet_id"
            @close-reply="() => { xweetToReply = null }" />
    </div>
    <MoreXweet />
    <Empty 
        v-if="timeline.length === 0"
        msg="This is where your timeline would appear" 
        submsg="Start following some people to get contents to your desire!" />
    <Modal :show="showModal" @clicked-outside="() => { showModal = false }">
        <section class="w-[50vw] h-36 flex flex-col items-center gap-4  bg-sky-800/20 text-white">
            <div class="w-full py-2 font-semibold text-center bg-red-600/60">
                <font-awesome-icon icon="fa-solid fa-spinner" spin-pulse v-if="isLoading" />
                <p>{{ isLoading ? '' : isError ? 'Failed to delete xweet. Please try again.' : 'Delete Xweet' }}</p>
            </div>
            <p>Are you sure you want to delete this xweet?</p>
            <div class="flex items-center justify-center gap-4">
                <button 
                    class="w-16 py-1 rounded-md bg-red-600/60 hover:bg-red-600 active:shadow-inner" 
                    title="Confirm delete" 
                    @click="deleteXweet(xweetToDelete)">
                    Yes
                </button>
                <button 
                    class="w-16 py-1 border border-solid rounded-md border-red-600/60 hover:border-red-600" 
                    title="Cancel"
                    @click="() => { showModal = false }">
                    No
                </button>
            </div>
        </section>
    </Modal>
</template>