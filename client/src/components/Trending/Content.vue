<script setup lang="ts">
import { Ref } from 'vue';

import Xweets from './Xweets.vue';
import Sep from '@/components/App/Sep.vue';
import Popup from '@/components/App/Popup.vue';
import useNotify from '@/composables/useNotify'

let notification: Ref<{
    isNotified: boolean
    category: "success" | "error" | undefined | null
    msg: string
}>

const showNotice = (category: 'success' | 'error', msg: string) => {
    notification = useNotify(category, msg)
}
</script>

<template>
    <Sep title="Topic:" :subtitle="`${$route.query.tag}`" is-sticky />
    <Xweets :show-notice="showNotice" />
    <Popup
        :show="notification.isNotified"
        :category="notification.category" 
        :message="notification.msg" />
</template>