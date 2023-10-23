<script setup lang="ts">
import { ref, watch, Ref } from 'vue';
import { useRoute } from 'vue-router';
import { useScroll } from '@vueuse/core';

import Xweet from '@/components/App/Xweet/index.vue';
import ReplyXweet from '@/components/App/Xweet/ReplyXweet.vue';
import MoreXweet from '@/components/App/Xweet/MoreXweet.vue';
import Empty from '@/components/App/Empty.vue';
import useAuthStore from '@/stores/useAuthStore';
import { ProfileTimeline } from '@/types/timeline';
import { LikeDetail } from '@/types/likes'
import { RexweetDetail } from '@/types/rexweets'
import socket from '@/utils/socket';
import { useFetchList } from '@/composables/useFetch';

defineProps<{
    y: number
    showNotice: (category: 'success' | 'error', msg: string) => void
}>()

const authStore = useAuthStore()

const route = useRoute()

const start = ref(0)
const timelineData = await useFetchList<ProfileTimeline>(
    `/api/users/${route.params.id}/profile-timeline?start=${start.value}`, false
    )
const timeline = timelineData.list

socket.on('add_to_timeline', (xweet) => {
    timeline.value.unshift(xweet)
})

const likes: Ref<number[]> = ref([])
const rexweets: Ref<number[]> = ref([])

if (authStore.getIsAuthenticated) {
    const likesData = await useFetchList<LikeDetail>(
        `/api/users/${authStore.getSignedInUserId}/likes`, true
        )
    const rexweetsData = await useFetchList<RexweetDetail>(
        `/api/users/${authStore.getSignedInUserId}/rexweets`, true
    )

    likesData.list.value.forEach(like => {
        likes.value.push(like.xweet_id)
    })
    rexweetsData.list.value.forEach(rexweet => {
        rexweets.value.push(rexweet.xweet_id)
    })
}

const xweetToReply = ref<number | null>()
// const xweetToDelete = ref<number | null>()
const isLoading = ref(false)

const timelineRef = ref<HTMLElement | null>(null)
const { arrivedState } = useScroll(timelineRef)
const needMoreXweet = ref(true)

watch(() => arrivedState.bottom, async () => {
    if (needMoreXweet) {
        start.value+= 10
        isLoading.value = true
    
        const newTimelineData = await useFetchList<ProfileTimeline>(
            `/api/users/${route.params.id}/profile-timeline?start=${start.value}`, false
        )
        const newTimeline = newTimelineData.list
        isLoading.value = false
    
        if (newTimeline.value.length === 0) {
            needMoreXweet.value = false
        } else {
            timeline.value.push(...newTimeline.value)
        }
    }
})
</script>

<template>
    <section class="flex flex-col max-h-screen gap-4 overflow-y-scroll scrollbar-hide" ref="timelineRef">
        <div v-for="xweet in timeline">
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
                :rexweeted="rexweets.includes(xweet.xweet_id)"
                :liked="likes.includes(xweet.xweet_id)"
                @show-notice="showNotice"
                @reply="(xweetId) => { xweetToReply = xweetId }" />
            <ReplyXweet 
                :show="xweetToReply === xweet.xweet_id"
                :xweet-id="xweet.xweet_id"
                @close-reply="() => { xweetToReply = null }" />
        </div>
        <MoreXweet v-if="needMoreXweet" :is-loading="isLoading" />
        <Empty 
            v-if="timeline.length === 0"
            msg="This is where your timeline would appear" 
            submsg="Start following some people to get contents to your desire!" />
    </section>
</template>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
    display: none;
}
.scrollbar-hide {
    -ms-overflow-style: none; 
    scrollbar-width: none;
}
</style>