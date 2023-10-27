<script setup lang="ts">
import { ref } from 'vue';

import Xweets from './Xweets.vue';
import Sep from '@/components/App/Sep.vue';
import Popup from '@/components/App/Popup.vue';
import useNotify from '@/composables/useNotify'

const notification = ref({ 
    isNotified: false, 
    category: undefined, 
    msg: '' 
    })

const showNotice = (category: 'success' | 'error', msg: string) => {
    useNotify(notification, category, msg)
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