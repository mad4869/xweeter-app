<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { TransitionRoot } from '@headlessui/vue';

import useAuth from '@/composables/useAuth';
import { sendReqCookie } from '@/utils/axiosInstances';
import { XweetResponse } from '@/types/xweets'

const { xweet_id, body, fileUrl } = defineProps<{
    show: boolean,
    xweet_id: number,
    body: string
    fileUrl?: string
}>()

const emit = defineEmits<{
    (e: 'update-xweet', newBody: string, updateDate?: string): void
}>()

const authStore = useAuth()

const MAX_CHARS = 140

const newBody = ref(body)
const charCount = computed(() => newBody.value.length)
const hashtags = computed(() => {
    const words = newBody.value.split(' ');
    return words.filter(word => word.startsWith('#')).map(word => word.replace('#', ''));
})

const textareaRef = ref<HTMLTextAreaElement | null>(null)

const isLoading = ref(false)
const isError = ref(false)
const isSuccess = ref(false)
const newFileUrl = ref(fileUrl)

const payload = computed(() => ({
    body: newBody.value,
    media: newFileUrl.value,
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
            }, 3000)
        }
    } catch (err) {
        isError.value = true

        setTimeout(() => {
            isError.value = false
        }, 3000)

        console.error(err)
    }
}

const manageFile = (e: Event) => {
    const target = e.target as HTMLInputElement
    const file = target.files?.[0]

    if (file) {
        const reader = new FileReader()

        reader.onload = (e: ProgressEvent<FileReader>) => {
            if (e.target instanceof FileReader) {
                newFileUrl.value = e.target.result as string
            }
        }

        reader.readAsDataURL(file)
    }
}

const removeFile = () => {
    newFileUrl.value = ''
}

onMounted(() => {
    textareaRef.value?.focus()
})
</script>

<template>
    <TransitionRoot
        :show="show" 
        as="section" 
        class="flex flex-col justify-between items-center h-full"
        enter="transition-opacity duration-200"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="transition-opacity duration-150"
        leave-from="opacity-100"
        leave-to="opacity-0">
        <textarea
            ref="textareaRef" 
            name="edit-xweet" 
            id="edit-xweet" 
            placeholder="What's on your mind..." 
            spellcheck="false"
            v-model="newBody"
            class="w-full h-10 px-4 py-2 bg-sky-200 rounded-lg caret-sky-800 resize-none transition-[height] duration-300 ease-out placeholder:text-sky-400 focus:h-32 focus:outline-none dark:bg-slate-200 dark:placeholder:text-slate-400"
            :class="charCount > MAX_CHARS ? 'text-red-600 focus-visible:outline-red-600' : 'text-slate-700 focus-visible:outline-sky-600'">
        </textarea>
        <div class="w-full py-4 flex justify-between items-start">
            <div class="flex items-center gap-2 h-full">
                <label for="edit-image" title="Edit image in your xweet">
                    <span
                        class="flex items-center gap-2 px-2 py-1 bg-sky-800/50 text-xs text-white rounded-md transition-colors cursor-pointer hover:bg-sky-800 dark:bg-sky-400/50 dark:hover:bg-sky-400">
                        <font-awesome-icon icon="fa-solid fa-images" />
                        <h6>Image</h6>
                    </span>
                    <input 
                        type="file" 
                        id="edit-image" 
                        alt="Edit Image" 
                        accept="image/jpeg, image/png" 
                        class="hidden"
                        @change="manageFile">
                </label>
                <div v-if="newFileUrl" class="relative group">
                    <img :src="newFileUrl" class="w-8 h-8 object-scale-down" />
                    <font-awesome-icon 
                        icon="fa-regular fa-circle-xmark" 
                        title="Remove the image"
                        class="absolute -top-1 -right-1 text-xs text-sky-800 cursor-pointer dark:text-white hidden group-hover:block"
                        @click.prevent="removeFile" />
                </div>
            </div>
            <div class="flex items-center h-full px-2 text-center dark:text-white">
                <p class="text-xs" v-if="charCount <= MAX_CHARS && !isSuccess && !isLoading">
                    <span>{{ charCount }}</span>
                    /
                    <span class="text-sky-800 dark:text-sky-600">{{ MAX_CHARS }}</span>
                </p>
                <TransitionRoot 
                    :show="charCount > MAX_CHARS"
                    as="p"
                    class="text-red-600 dark:text-red-400"
                    enter="transition-opacity duration-200"
                    enter-from="opacity-0"
                    enter-to="opacity-100"
                    leave="transition-opacity duration-150"
                    leave-from="opacity-100"
                    leave-to="opacity-0">
                    Your xweet exceeds the maximum number of characters
                </TransitionRoot>
                <TransitionRoot 
                    :show="isSuccess"
                    as="p"
                    class="text-sky-800 font-bold opacity-0 dark:text-sky-600"
                    enter="transition-opacity duration-200"
                    enter-from="opacity-0"
                    enter-to="opacity-100"
                    leave="transition-opacity duration-150"
                    leave-from="opacity-100"
                    leave-to="opacity-0">
                    You have fixed your xweet!
                </TransitionRoot>
            </div>
            <div class="flex items-center gap-2 h-full">
                <font-awesome-icon 
                    v-if="isLoading"
                    icon="fa-solid fa-spinner" spin-pulse 
                    class="text-white" />
                <input type="button" value="Fix Xweet"
                    class="px-4 py-1 bg-sky-600 text-white font-semibold rounded-md transition-colors duration-200 cursor-pointer hover:bg-sky-800 active:shadow-inner disabled:bg-slate-800 disabled:text-slate-600 disabled:cursor-not-allowed"
                    :disabled="charCount > MAX_CHARS || (charCount === 0 && !newFileUrl) || isLoading" 
                    title="Add new xweet" 
                    @mousedown.prevent="editXweet">
            </div>
        </div>
    </TransitionRoot>
</template>