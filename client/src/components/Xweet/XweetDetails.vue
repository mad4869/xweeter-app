<script setup lang="ts">
import { ref } from 'vue';

import Replies from './Replies.vue';
import Xweet from '@/components/App/Xweet/index.vue';
import ReplyXweet from '@/components/App/Xweet/ReplyXweet.vue';
import useAuthStore from '@/stores/useAuthStore';
import { XweetDetail } from '@/types/xweets';

defineProps<{
    data: XweetDetail | undefined
}>()

const authStore = useAuthStore()

const isRepliable = ref(false)
const showReplyEditor = (xweetId: number | null) => {
    if (!xweetId) {
        isRepliable.value = false
    } else {
        isRepliable.value = true
    }
}
</script>

<template>
    <section class="flex flex-col">
        <Xweet
            :key="data?.xweet_id"
            :id="data?.xweet_id!"
            :userId="data?.user_id!"
            :fullname="data?.full_name!" 
            :username="data?.username!" 
            :body="data?.body!" 
            :media="data?.media"
            :profilePic="data?.profile_pic" 
            :createdAt="data?.created_at!" 
            :updated-at="data?.updated_at" 
            :is-rexweet="false"
            :is-reply="false"
            :is-own="data?.user_id === authStore.getSignedInUserId" 
            :rexweeted="false"
            :liked="false"
            @reply="showReplyEditor" />
        <ReplyXweet
            class="mt-4" 
            :show="isRepliable"
            :xweet-id="(data?.xweet_id as number)"
            @close-reply="isRepliable = false" />
        <Replies />
    </section>
</template>