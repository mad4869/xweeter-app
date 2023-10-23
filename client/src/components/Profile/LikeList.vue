<script setup lang="ts">
import { ref, watch, Ref } from 'vue';
import { useRoute } from 'vue-router';
import { useScroll } from '@vueuse/core';

import Xweet from '@/components/App/Xweet/index.vue';
import ReplyXweet from '@/components/App/Xweet/ReplyXweet.vue';
import MoreXweet from '@/components/App/Xweet/MoreXweet.vue';
import Empty from '@/components/App/Empty.vue';
import useAuthStore from '@/stores/useAuthStore';
import { LikeDetail} from '@/types/likes'
import { RexweetDetail } from '@/types/rexweets'
import { useFetchList } from '@/composables/useFetch';

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
const likesData = await useFetchList<LikeDetail>(`/api/users/${route.params.id}/likes?start=${start.value}`, false)
const likes = likesData.list

const userLikes: Ref<number[]> = ref([])
const userRexweets: Ref<number[]> = ref([])

if (authStore.getIsAuthenticated) {
    const userLikesData = await useFetchList<LikeDetail>(`/api/users/${authStore.getSignedInUserId}/likes`, true)
    const userRexweetsData = await useFetchList<RexweetDetail>(`/api/users/${authStore.getSignedInUserId}/rexweets`, true)
    
    userLikesData.list.value.forEach(like => {
        userLikes.value.push(like.xweet_id)
    })
    userRexweetsData.list.value.forEach(rexweet => {
        userRexweets.value.push(rexweet.xweet_id)
    })
}

const xweetToReply = ref<number | null>()
const isLoading = ref(false)

const likeRef = ref<HTMLElement | null>(null)
const { arrivedState } = useScroll(likeRef)

const needMoreXweet = ref(true)
if (likes.value.length <= 4) {
    needMoreXweet.value = false
}

watch(() => arrivedState.bottom, async () => {
    if (needMoreXweet) {
        start.value+= 10
        isLoading.value = true
    
        const newLikesData = await useFetchList<LikeDetail>(
            `/api/users/${route.params.id}/likes?start=${start.value}`, false
            )
        const newLikes = newLikesData.list
        isLoading.value = false
    
        if (newLikes.value.length === 0) {
            needMoreXweet.value = false
        } else {
            likes.value.push(...newLikes.value)
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
                :is-rexweet="false"
                :is-own="xweet.user_id === authStore.getSignedInUserId" 
                :rexweeted="userRexweets.includes(xweet.xweet_id)"
                :liked="userLikes.includes(xweet.xweet_id)"
                @show-notice="showNotice"
                @reply="(xweetId) => { xweetToReply = xweetId }" />
            <ReplyXweet 
                :show="xweetToReply === xweet.xweet_id"
                :xweet-id="xweet.xweet_id"
                @close-reply="xweetToReply = null" />
        </div>
        <MoreXweet v-if="needMoreXweet" :is-loading="isLoading" />
        <Empty 
            v-if="likes.length === 0"
            msg="There are no likes yet" />
    </section>
</template>