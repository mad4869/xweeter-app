<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';

import Layout from '@/components/App/Layout/index.vue'
import SidebarLeft from '@/components/App/Layout/SidebarLeft.vue';
import SidebarRight from '@/components/App/Layout/SidebarRight.vue';
import Skeleton from '@/components/App/Skeleton/index.vue'
import Xweet from '@/components/App/Xweet/index.vue';
import ReplyXweet from '@/components/App/Xweet/ReplyXweet.vue';
import Sep from '@/components/App/Sep.vue';
import Modal from '@/components/App/Modal.vue';
import NewXweet from '@/components/App/Xweet/NewXweet.vue';
import useAuthStore from '@/stores/useAuthStore';
import { countStore } from '@/stores/useCountStore';
import { XweetDetail } from '@/types/xweets';
import { Reply } from '@/types/replies'
import { useFetchList, useFetchObject } from '@/composables/useFetch';

const authStore = useAuthStore()
await authStore.getUser()

const route = useRoute()

const xweet = await useFetchObject<XweetDetail>(`/api/xweets/${route.params.id}`, false)
const replies = await useFetchList<Reply>(`/api/xweets/${route.params.id}/replies`, false)

const isRepliable = ref(false)
const showReplyEditor = (xweetId: number | null) => {
    if (!xweetId) {
        isRepliable.value = false
    } else {
        isRepliable.value = true
    }
}

const showModal = ref(false)
</script>

<template>
    <Suspense>
        <Layout>
            <template #sidebarLeft>
                <SidebarLeft @show-new-xweet="showModal = true" />
            </template>
            <Sep title="Xweet from:" :subtitle="`@${xweet.obj.value?.username}`" :is-sticky="false" />
            <div class="flex flex-col">
                <Xweet
                    :key="xweet.obj.value?.xweet_id"
                    :id="xweet.obj.value?.xweet_id!"
                    :userId="xweet.obj.value?.user_id!"
                    :fullname="xweet.obj.value?.full_name!" 
                    :username="xweet.obj.value?.username!" 
                    :body="xweet.obj.value?.body!" 
                    :media="xweet.obj.value?.media"
                    :profilePic="xweet.obj.value?.profile_pic" 
                    :createdAt="xweet.obj.value?.created_at!" 
                    :updated-at="xweet.obj.value?.updated_at" 
                    :is-rexweet="false"
                    :is-reply="false"
                    :is-own="xweet.obj.value?.user_id === authStore.getSignedInUserId" 
                    :rexweeted="false"
                    :liked="false"
                    @reply="showReplyEditor" />
                <ReplyXweet
                    class="mt-4" 
                    :show="isRepliable"
                    :xweet-id="(xweet.obj.value?.xweet_id as number)"
                    @close-reply="isRepliable = false" />
                <Sep v-if="replies.list.value.length > 0" title="Replies" is-sticky />
                <div class="flex flex-col gap-2">
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
                </div>
            </div>
            <Modal :show="showModal" @clicked-outside="showModal = false">
                <NewXweet in-modal 
                    @increment-xweet-count="countStore.incrementXweetsCount()"
                    @close-modal="showModal = false" />
            </Modal>
            <template #sidebarRight>
                <SidebarRight />
            </template>
        </Layout>
        <template #fallback>
            <Skeleton />
        </template>
    </Suspense>
</template>