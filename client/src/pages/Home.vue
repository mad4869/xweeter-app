<script setup lang="ts">
import Layout from '@/components/App/Layout/index.vue'
import SidebarLeft from '@/components/App/Layout/SidebarLeft.vue';
import SidebarRight from '@/components/App/Layout/SidebarRight.vue';
import Skeleton from '@/components/App/Skeleton/index.vue'
import Content from '@/components/Home/Content.vue';
import useAuthStore from '@/stores/useAuthStore';

const authStore = useAuthStore()
await authStore.getUser()
</script>

<template>
    <Suspense>
        <Layout>
            <template #sidebarLeft>
                <SidebarLeft />
            </template>
            <Content />
            <template #sidebarRight>
                <SidebarRight />
            </template>
        </Layout>
        <template #fallback>
            <Skeleton />
        </template>
    </Suspense>
</template>