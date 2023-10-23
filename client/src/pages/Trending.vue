<script setup lang="ts">
import { useRoute } from 'vue-router';

import Layout from '@/components/App/Layout/index.vue'
import SidebarRight from '@/components/App/Layout/SidebarRight.vue';
import SidebarLeft from '@/components/App/Layout/SidebarLeft.vue';
import Skeleton from '@/components/App/Skeleton/index.vue'
import Xweet from '@/components/App/Xweet/index.vue';
import Sep from '@/components/App/Sep.vue';
import useAuthStore from '@/stores/useAuthStore';
import { XweetDetail } from '@/types/xweets';
import { useFetchList } from '@/composables/useFetch';

const authStore = useAuthStore()
await authStore.getUser()

const route = useRoute()

const trending = await useFetchList<XweetDetail>(`/api/hashtags/${route.query.tag}`, false)
</script>

<template>
    <Suspense>
        <Layout>
            <template #sidebarLeft>
                <SidebarLeft />
            </template>
            <Sep title="Topic:" :subtitle="`${$route.query.tag}`" is-sticky />
            <Xweet v-for="xweet in trending.list.value"
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
                :liked="false" />
            <template #sidebarRight>
                <SidebarRight />
            </template>
        </Layout>
        <template #fallback>
            <Skeleton />
        </template>
    </Suspense>
</template>