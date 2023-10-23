<script setup lang="ts">
import { useRoute } from 'vue-router';

import XweetDetails from './XweetDetails.vue';
import Sep from '@/components/App/Sep.vue';
import { useFetchObject } from '@/composables/useFetch';
import { XweetDetail } from '@/types/xweets';

const route = useRoute()

const xweet = await useFetchObject<XweetDetail>(`/api/xweets/${route.params.id}`, false)
</script>

<template>
    <Sep title="Xweet from:" :subtitle="`@${xweet.obj.value?.username}`" :is-sticky="false" />
    <XweetDetails :data="xweet.obj.value" />
</template>