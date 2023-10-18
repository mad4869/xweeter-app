<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useScroll } from '@vueuse/core';

import Timeline from './Timeline.vue'
import NewXweet from '@/components/App/Xweet/NewXweet.vue';
import Sep from '@/components/App/Sep.vue';
import Popup from '@/components/App/Popup.vue'
import useAuthStore from '@/stores/useAuthStore';
import { countStore } from '@/stores/useCountStore'

const authStore = useAuthStore()

const el = ref<HTMLElement | null>(null)
const { y } = useScroll(el)

const notification = reactive<{
    isNotified: boolean,
    category?: 'success' | 'error'
    msg: string
}>({
    isNotified: false,
    msg: ''
})

const showNotice = (category: 'success' | 'error', msg: string) => {
    notification.isNotified = true
    notification.category = category
    notification.msg = msg

    setTimeout(() => {
        notification.isNotified = false
        notification.msg = ''
    }, 3000)
}
</script>

<template>
    <NewXweet 
        v-if="authStore.getIsAuthenticated" 
        @increment-xweet-count="() => { countStore.incrementXweetsCount() }" />
    <Sep title="Timeline" is-sticky class="cursor-pointer" @click="() => { y = 0 }" />
    <Timeline :y="y" :show-notice="showNotice" @show-notice="showNotice" />
    <Popup 
        :show="notification.isNotified" 
        :message="(notification.msg as string)" 
        :category="notification.category" />
</template>