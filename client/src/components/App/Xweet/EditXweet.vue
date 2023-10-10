<script setup lang="ts">
import { computed, ref } from 'vue';

import TextEditor from './TextEditor.vue';
import Toolbar from './Toolbar.vue';
import useRenderHashtags from '@/composables/useRenderHashtags';
import useAuthStore from '@/stores/useAuthStore';
import { MAX_CHAR_COUNT } from '@/utils/constants';
import { sendReqCookie } from '@/utils/axiosInstances';
import { XweetResponse } from '@/types/xweets'

const { xweet_id, body, fileUrl } = defineProps<{
    xweet_id: number,
    body: string
    fileUrl?: string
}>()

const emit = defineEmits<{
    (e: 'update-xweet', newBody: string, newMedia?: string, updateDate?: string): void
}>()

const authStore = useAuthStore()

const newBody = ref(body)
const newMedia = ref(fileUrl)
const charCount = computed(() => newBody.value.length)
const hashtags = useRenderHashtags(newBody)

const payload = computed(() => ({
    body: newBody.value,
    media: newMedia.value,
    hashtags: hashtags.value
}))

const isLoading = ref(false)
const isSuccess = ref(false)

const editXweet = async () => {
    isLoading.value = true

    try {
        const { data } = await sendReqCookie.put<XweetResponse | undefined>(
            `/api/users/${authStore.getSignedInUserId}/xweets/${xweet_id}`, payload.value
        )

        if (data?.success) {
            isLoading.value = false
            isSuccess.value = true
            newBody.value = ''
            newMedia.value = ''
            
            setTimeout(() => {
                isSuccess.value = false

                emit('update-xweet', data.data.body, data.data.media, data.data.updated_at)
            }, 1000)
        }
    } catch (err) {
        console.error(err)
    }
}

const setMedia = (fileUrl: string) => {
    newMedia.value = fileUrl
}
</script>

<template>
    <section class="flex flex-col justify-between items-center h-full">
        <TextEditor
            input-name="edit-xweet"
            v-model="newBody"
            :char-count="charCount"
            :max-char-count="MAX_CHAR_COUNT" />
        <Toolbar
            mode="edit-xweet"
            :submit-func="editXweet"
            :is-loading="isLoading"
            :is-success="isSuccess"
            :char-count="charCount"
            :max-char-count="MAX_CHAR_COUNT"
            :media="newMedia"
            @set-media="setMedia" />
    </section>
</template>