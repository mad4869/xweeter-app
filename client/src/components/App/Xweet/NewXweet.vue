<script setup lang="ts">
import { computed, ref } from 'vue'

import Toolbar from './Toolbar.vue'
import TextEditor from './TextEditor.vue'
import useRenderHashtags from '@/composables/useRenderHashtags'
import useAuthStore from '@/stores/useAuthStore'
import socket from '@/utils/socket'
import { sendReqCookie } from '@/utils/axiosInstances'
import { MAX_CHAR_COUNT } from '@/utils/constants'
import { XweetResponse } from '@/types/xweets'

const { inModal } = defineProps({
    inModal: {
        type: Boolean,
        default: false
    }
})
const emit = defineEmits<{
    (e: 'increment-xweet-count'): void
    (e: 'close-modal'): void
}>()

const authStore = useAuthStore()

const body = ref('')
const media = ref('')
const charCount = computed(() => body.value.length)
const hashtags = useRenderHashtags(body)

const payload = computed(() => ({
    body: body.value,
    media: media.value,
    hashtags: hashtags.value
}))

const isLoading = ref(false)
const isSuccess = ref(false)

const addXweet = async () => {
    isLoading.value = true

    try {
        const { data } = await sendReqCookie.post<XweetResponse | undefined>(
            `/api/users/${authStore.getSignedInUserId}/xweets`, payload.value
        )

        if (data?.success) {
            socket.emit('add_to_timeline', authStore.getSignedInUserId)
            emit('increment-xweet-count')

            isLoading.value = false
            isSuccess.value = true
            body.value = ''
            media.value = ''

            setTimeout(() => {
                isSuccess.value = false
                if (inModal) {
                    emit('close-modal')
                }
            }, 1000)
        }
    } catch (err) {
        console.error(err)
    }
}
</script>

<template>
    <section 
        class="relative flex flex-col justify-between items-center min-w-[50vw] px-12 border border-solid border-sky-800 rounded-xl">
        <span class="w-full py-4 text-2xl text-sky-950 dark:text-white">New Xweet</span>
        <TextEditor
            :input-name="!inModal ? 'new-xweet' : 'modal-new-xweet'"
            v-model="body"
            :char-count="charCount"
            :max-char-count="MAX_CHAR_COUNT" />
        <Toolbar
            :mode="!inModal ? 'new-xweet' : 'modal-new-xweet'"
            :submit-func="addXweet"
            :is-loading="isLoading"
            :is-success="isSuccess"
            :char-count="charCount"
            :max-char-count="MAX_CHAR_COUNT"
            :media="media"
            @set-media="(fileUrl: string) => { media = fileUrl }" />
    </section>
</template>