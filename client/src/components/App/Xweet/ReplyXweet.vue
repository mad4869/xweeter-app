<script setup lang="ts">
import { ref, computed } from 'vue';
import { TransitionRoot } from '@headlessui/vue';

import TextEditor from './TextEditor.vue';
import Toolbar from './Toolbar.vue';
import useAuthStore from '@/stores/useAuthStore';
import { countStore } from '@/stores/useCountStore';
import { sendReqCookie } from '@/utils/axiosInstances'
import { MAX_CHAR_COUNT } from '@/utils/constants'
import { RepliesResponse } from '@/types/replies';

const { xweetId } = defineProps<{
    show: boolean
    xweetId: number
}>()
const emit = defineEmits<{
    (e: 'increment-reply-count'): void
    (e: 'close-reply'): void
}>()

const authStore = useAuthStore()

const body = ref('')
const media = ref('')
const charCount = computed(() => body.value.length)

const payload = computed(() => ({
    xweet_id: xweetId,
    body: body.value,
    media: media.value,
}))

const isLoading = ref(false)
const isSuccess = ref(false)

const replyXweet = async () => {
    isLoading.value = true

    try {
        const { data } = await sendReqCookie.post<RepliesResponse | undefined>(
            `/api/users/${authStore.getSignedInUserId}/replies`, payload.value
        )

        if (data?.success) {
            isLoading.value = false
            isSuccess.value = true
            body.value = ''
            media.value = ''

            setTimeout(() => {
                isSuccess.value = false
                
                countStore.incrementRepliesCount()
                emit('close-reply')
            }, 1000)
        }
    } catch (err) {
        console.error(err)
    }
}
</script>

<template>
    <TransitionRoot
        as="section"
        :show="show"
        class="px-8 pt-4 flex flex-col justify-center items-center bg-sky-600/10 backdrop-blur-lg border border-solid border-sky-800 rounded-xl before:absolute before:top-0 before:left-16 before:-translate-y-2 before:w-0 before:h-0 before:border-l-8 before:border-r-8 before:border-b-8 before:border-solid before:border-l-transparent before:border-r-transparent before:border-b-sky-800"
        enter="transition-all duration-500 ease-out"
        enter-from="-translate-y-1 opacity-0"
        enter-to="translate-y-0 opacity-100"
        leave="transition-all duration-150 ease-in"
        leave-from="translate-y-0 opacity-100"
        leave-to="-translate-y-1 opacity-0">
        <TextEditor
            input-name="reply-xweet"
            v-model="body"
            :char-count="charCount"
            :max-char-count="MAX_CHAR_COUNT" />
        <Toolbar
            mode="reply-xweet"
            :submit-func="replyXweet"
            :is-loading="isLoading"
            :is-success="isSuccess"
            :char-count="charCount"
            :max-char-count="MAX_CHAR_COUNT"
            :media="media"
            @set-media="(fileUrl: string) => { media = fileUrl }" />
    </TransitionRoot>
</template>