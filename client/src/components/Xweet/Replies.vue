<script setup lang="ts">
import { useRoute } from 'vue-router';

import Sep from '@/components/App/Sep.vue';
import Xweet from '@/components/App/Xweet/index.vue';
import { useFetchList } from '@/composables/useFetch';
import useAuthStore from '@/stores/useAuthStore';
import { Reply } from '@/types/replies'

const authStore = useAuthStore()

const route = useRoute()

const replies = await useFetchList<Reply>(`/api/xweets/${route.params.id}/replies`, false)
</script>

<template>
    <Sep v-if="(replies.list.value?.length ?? 0) > 0" title="Replies" is-sticky />
    <section class="flex flex-col gap-2">
        <Xweet v-for="reply in replies.list.value"
            :key="reply.xweet_id"
            :id="reply.xweet_id!"
            :userId="reply.user_id!"
            :fullname="reply.full_name!" 
            :username="reply.username!" 
            :body="reply.body!" 
            :media="reply.media"
            :profilePic="reply.profile_pic" 
            :createdAt="reply.created_at!" 
            :updated-at="reply.updated_at" 
            :is-rexweet="false"
            :is-reply="true"
            :is-own="reply.user_id === authStore.getSignedInUserId" 
            :rexweeted="false"
            :liked="false" />
    </section>
</template>