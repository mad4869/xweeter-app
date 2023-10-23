<script setup lang="ts">
import { ref } from 'vue';

import Layout from '@/components/App/Layout/index.vue'
import SidebarLeft from '@/components/App/Layout/SidebarLeft.vue';
import SidebarRight from '@/components/App/Layout/SidebarRight.vue';
import Skeleton from '@/components/App/Skeleton/index.vue'
import Sep from '@/components/App/Sep.vue';
import Table from '@/components/Leaderboard/Table.vue';
import Pagination from '@/components/Leaderboard/Pagination.vue';
import Modal from '@/components/App/Modal.vue';
import NewXweet from '@/components/App/Xweet/NewXweet.vue';
import useAuthStore from '@/stores/useAuthStore';
import { countStore } from '@/stores/useCountStore';
import { TopDailyUserData } from '@/types/users'
import { useFetchObject } from '@/composables/useFetch';

const authStore = useAuthStore()
await authStore.getUser()

const topUsers = await useFetchObject<TopDailyUserData>('/api/users/most-active-daily', false)

const showModal = ref(false)
</script>

<template>
    <Suspense>
        <Layout>
            <template #sidebarLeft>
                <SidebarLeft @show-new-xweet="showModal = true" />
            </template>
            <Sep is-sticky title="Top Daily Users" />
            <Table :data="topUsers.obj.value?.users" />
            <Pagination :pages="topUsers.obj.value?.total_pages" />
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