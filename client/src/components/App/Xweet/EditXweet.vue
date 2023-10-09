<script setup lang="ts">
import { computed, ref } from 'vue';

import TextEditor from './TextEditor.vue';
import Toolbar from './Toolbar.vue';
import useAuth from '@/composables/useAuth';
import { MAX_CHAR_COUNT } from '@/utils/constants';
import { sendReqCookie } from '@/utils/axiosInstances';
import { XweetResponse } from '@/types/xweets'

const { xweet_id, body, fileUrl } = defineProps<{
    xweet_id: number,
    body: string
    fileUrl?: string
}>()

const emit = defineEmits<{
    (e: 'update-xweet', newBody: string, updateDate?: string): void
}>()

const authStore = useAuth()

const newBody = ref(body)
const charCount = computed(() => newBody.value.length)
const hashtags = computed(() => {
    const words = newBody.value.split(' ');
    return words.filter(word => word.startsWith('#')).map(word => word.replace('#', ''));
})

// const textareaRef = ref<HTMLTextAreaElement | null>(null)

const isLoading = ref(false)
const isSuccess = ref(false)
const media = ref(fileUrl)

const payload = computed(() => ({
    body: newBody.value,
    media: media.value,
    hashtags: hashtags.value
}))

const editXweet = async () => {
    isLoading.value = true

    try {
        const { data } = await sendReqCookie.put<XweetResponse | undefined>(
            `/api/users/${authStore.getSignedInUserId}/xweets/${xweet_id}`, payload.value
        )

        if (data?.success) {
            isLoading.value = false
            isSuccess.value = true
            
            setTimeout(() => {
                isSuccess.value = false

                emit('update-xweet', data.data.body, data.data.updated_at)
            }, 1000)
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
    <section class="flex flex-col justify-between items-center h-full">
        <TextEditor
            input-id="edit-xweet"
            input-name="edit-xweet"
            ref="textareaRef"
            v-model="newBody"
            :char-count="charCount"
            :max-char-count="MAX_CHAR_COUNT" />
        <Toolbar
            mode="edit-xweet"
            :submit-func="editXweet"
            :is-loading="isLoading"
            :is-success="isSuccess"
            :show-media-preview="media !== ''"
            :char-count="charCount"
            :max-char-count="MAX_CHAR_COUNT"
            @send-file="manageFile" />
    </section>
</template>