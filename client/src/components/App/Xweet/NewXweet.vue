<script setup lang="ts">
import { computed, ref } from 'vue'

import TextEditor from '@/components/App/Xweet/TextEditor.vue'
import Toolbar from './Toolbar.vue'
import useAuth from '@/composables/useAuth'
import socket from '@/utils/socket'
import { sendReqCookie } from '@/utils/axiosInstances'
import { XweetResponse } from '@/types/xweets'

const authStore = useAuth()

const body = ref('')
const charCount = computed(() => body.value.length)
const maxCharCount = 140
const media = ref('')
const hashtags = computed(() => {
    const words = body.value.split(' ');
    return words.filter(word => word.startsWith('#')).map(word => word.replace('#', ''));
})

const isLoading = ref(false)
const isSuccess = ref(false)

const payload = computed(() => ({
    user_id: authStore.getSignedInUserId,
    body: body.value,
    media: media.value,
    hashtags: hashtags.value
}))

const addXweet = async () => {
    isLoading.value = true

    try {
        const { data } = await sendReqCookie.post<XweetResponse | undefined>(
            `/api/users/${authStore.getSignedInUserId}/xweets`, payload.value
        )

        if (data?.success) {
            socket.emit('add_to_timeline', authStore.getSignedInUserId)

            isLoading.value = false
            isSuccess.value = true
            body.value = ''
            media.value = ''

            setInterval(() => {
                isSuccess.value = false
            }, 3000)
        }
    } catch (err) {
        console.error(err)
    }
}

const manageFile = (fileUrl: string) => {
    media.value = fileUrl
}
</script>

<template>
    <section 
        class="relative flex flex-col justify-between items-center min-w-[50vw] px-12 border border-solid border-sky-800 rounded-xl">
        <span class="w-full py-4 text-2xl text-sky-950 dark:text-white">New Xweet</span>
        <TextEditor
            input-id="new-xweet"
            input-name="new-xweet"
            v-model="body"
            :char-count="charCount"
            :max-char-count="maxCharCount" />
        <Toolbar
            mode="new-xweet"
            :submit-func="addXweet"
            :is-loading="isLoading"
            :is-success="isSuccess"
            :show-media-preview="media !== ''"
            :char-count="charCount"
            :max-char-count="maxCharCount"
            @send-file="manageFile" />
    </section>
</template>