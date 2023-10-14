<script setup lang="ts">
import { ref, reactive } from 'vue';

import Layout from '../components/App/Layout/index.vue'
import SidebarLeft from '@/components/App/Layout/SidebarLeft.vue';
import SidebarRight from '@/components/App/Layout/SidebarRight.vue';
import Modal from '@/components/App/Modal.vue';
import NewXweet from '@/components/App/Xweet/NewXweet.vue';
import Popup from '@/components/App/Popup.vue'
import Skeleton from '@/components/App/Skeleton/index.vue'
import Content from '@/components/Home/Content.vue';
import useAuthStore from '@/stores/useAuthStore';
import { countStore } from '@/stores/useCountStore'
import { XweetsResponse } from '@/types/xweets';
import { sendReqCookie } from '@/utils/axiosInstances';

const authStore = useAuthStore()
await authStore.getUser()

const getXweets = async (): Promise<XweetsResponse | undefined> => {
    try {
        if (authStore.getIsAuthenticated) {
            const { data } = await sendReqCookie.get(`/api/users/${authStore.getSignedInUserId}/xweets`)
            if (data) {
                return data
            }
        }
    } catch (err) {
        console.error(err)
    }
}

const { data } = (await getXweets()) || { data: [] }
countStore.xweetsCount = data.length

const notification = reactive<{
    isNotified: boolean,
    category: 'success' | 'error' | undefined
    msg: string
}>({
    isNotified: false,
    category: undefined,
    msg: ''
})

const showNotice = (category: 'success' | 'error', msg: string) => {
    notification.isNotified = true
    notification.category = category
    notification.msg = msg

    setTimeout(() => {
        notification.isNotified = false
        notification.category = undefined
        notification.msg = ''
    }, 3000)
}

const isModalShown = ref(false)
</script>

<template>
    <Suspense>
        <Layout>
            <template #sidebarLeft>
                <SidebarLeft :profile-props="{ showNewXweet: () => { isModalShown = true } }" />
            </template>
            <Content :show-notice="showNotice" @show-notice="showNotice" />
            <Modal :show="isModalShown" @clicked-outside="() => { isModalShown = false }">
                <NewXweet in-modal 
                    @increment-xweet-count="() => { countStore.incrementXweetsCount() }"
                    @close-modal="() => { isModalShown = false }" />
            </Modal>
            <Popup 
                :show="notification.isNotified" 
                :message="(notification.msg as string)" 
                :category="notification.category" />
            <template #sidebarRight>
                <SidebarRight />
            </template>
        </Layout>
        <template #fallback>
            <Skeleton />
        </template>
    </Suspense>
</template>