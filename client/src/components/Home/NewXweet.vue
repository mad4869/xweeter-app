<script setup lang="ts">
import { computed, ref } from 'vue';
// import { TransitionRoot } from '@headlessui/vue';

import useAuth from '../../composables/useAuth';
import socket from '../../utils/socket';
import { sendReqCookie } from '../../utils/axiosInstances';
import { XweetResponse } from '../../types/xweets'
import { ReplyResponse } from '../../types/replies'

const { xweetId } = defineProps({
    isReply: {
        type: Boolean,
        default: false
    },
    xweetId: {
        type: Number
    }
})

const authStore = useAuth()

const MAX_CHARS = 140

const body = ref('')
const charCount = computed(() => body.value.length)
const hashtags = computed(() => {
    const words = body.value.split(' ');
    return words.filter(word => word.startsWith('#')).map(word => word.replace('#', ''));
})

const isLoading = ref(false)
const isError = ref(false)
const isSuccess = ref(false)
const fileUrl = ref('')

const payload = computed(() => ({
    user_id: authStore.getSignedInUserId,
    body: body.value,
    media: fileUrl.value,
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
            fileUrl.value = ''

            setInterval(() => {
                isSuccess.value = false
            }, 3000)
        }
    } catch (err) {
        isError.value = true

        setInterval(() => {
            isError.value = false
        }, 3000)

        console.error(err)
    }
}

const replyXweet = async () => {
    isLoading.value = true

    try {
        const { data } = await sendReqCookie.post<ReplyResponse | undefined>(
            `/api/xweets/${xweetId}/replies`, payload.value
        )

        if (data?.success) {
            isLoading.value = false
            isSuccess.value = true
            body.value = ''
            fileUrl.value = ''

            setInterval(() => {
                isSuccess.value = false
            }, 3000)
        }
    } catch (err) {
        isError.value = true

        setInterval(() => {
            isError.value = false
        }, 3000)

        console.error(err)
    }
}

const addFile = (e: Event) => {
    const target = e.target as HTMLInputElement
    const file = target.files?.[0]

    if (file) {
        const reader = new FileReader()

        reader.onload = (e: ProgressEvent<FileReader>) => {
            if (e.target instanceof FileReader) {
                fileUrl.value = e.target.result as string
            }
        }

        reader.readAsDataURL(file)
    }
}

const removeFile = () => {
    fileUrl.value = ''
}
</script>

<template>
    <!-- <TransitionRoot
        :show="show"
        appear 
        as="section" 
        class="flex flex-col justify-between items-center h-full"
        enter="transition-opacity duration-200"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="transition-opacity duration-150"
        leave-from="opacity-100"
        leave-to="opacity-0"> -->
        <section 
            class="relative flex flex-col justify-between items-center min-w-[50vw] px-12 border border-solid border-sky-800 rounded-xl"
            :class="!isReply ? '' : 'pt-4 before:absolute before:top-0 before:left-16 before:-translate-y-2 before:w-0 before:h-0 before:border-l-8 before:border-r-8 before:border-b-8 before:border-solid before:border-l-transparent before:border-r-transparent before:border-b-sky-800'">
            <span v-if="!isReply" class="w-full py-4 text-2xl text-sky-950 dark:text-white">New Xweet</span>
            <textarea 
                name="new-xweet" 
                id="new-xweet" 
                placeholder="What's on your mind..." 
                spellcheck="false"
                v-model="body"
                class="w-full h-10 px-4 py-2 bg-sky-200 rounded-lg caret-sky-800 resize-none transition-[height] duration-300 ease-out placeholder:text-sky-400 focus:h-32 focus:outline-none dark:bg-slate-200 dark:placeholder:text-slate-400"
                :class="charCount > MAX_CHARS ? 'text-red-600 focus-visible:outline-red-600' : 'text-slate-700 focus-visible:outline-sky-600'">
            </textarea>
            <div class="w-full py-4 flex justify-between items-start">
                <div class="flex items-center gap-2 h-full">
                    <label for="add-image" title="Add image to your xweet">
                        <span
                            class="flex items-center gap-2 px-2 py-1 bg-sky-800/50 text-xs text-white rounded-md transition-colors cursor-pointer hover:bg-sky-800 dark:bg-sky-400/50 dark:hover:bg-sky-400">
                            <font-awesome-icon icon="fa-solid fa-images" />
                            <h6>Image</h6>
                        </span>
                        <input 
                            type="file" 
                            id="add-image" 
                            alt="Add Image" 
                            accept="image/jpeg, image/png" 
                            class="hidden"
                            @change="addFile">
                    </label>
                    <div v-if="fileUrl" class="relative group">
                        <img :src="fileUrl" class="w-8 h-8 object-scale-down" />
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
                    <p class="text-red-600 opacity-0 fade-in dark:text-red-400" v-if="charCount > MAX_CHARS">
                        Your xweet exceeds the maximum number of characters
                    </p>
                    <p class="text-sky-800 font-bold opacity-0 fade-in dark:text-sky-600" v-if="isSuccess">
                        {{ !isReply ? 'You posted a new xweet!' : 'You replied to the xweet!'}}
                    </p>
                </div>
                <div class="flex items-center gap-2 h-full">
                    <font-awesome-icon 
                        v-if="isLoading"
                        icon="fa-solid fa-spinner" spin-pulse 
                        class="text-white" />
                    <input v-if="!isReply" type="button" value="Xweet"
                        class="px-4 py-1 bg-sky-600 text-white font-semibold rounded-md transition-colors duration-200 cursor-pointer hover:bg-sky-800 active:shadow-inner disabled:bg-slate-800 disabled:text-slate-600 disabled:cursor-not-allowed"
                        :disabled="charCount > MAX_CHARS || (charCount === 0 && !fileUrl) || isLoading" 
                        title="Add new xweet" 
                        @mousedown.prevent="addXweet">
                    <input v-else type="button" value="Reply"
                        class="px-4 py-1 bg-sky-600 text-white font-semibold rounded-md transition-colors duration-200 cursor-pointer hover:bg-sky-800 active:shadow-inner disabled:bg-slate-800 disabled:text-slate-600 disabled:cursor-not-allowed"
                        :disabled="charCount > MAX_CHARS || (charCount === 0 && !fileUrl) || isLoading" 
                        title="Send reply"
                        @mousedown.prevent="replyXweet">
                </div>
            </div>
        </section>
    <!-- </TransitionRoot> -->
</template>

<style scoped>
.fade-in {
    animation: fade-in 200ms ease-in forwards;
}

@keyframes fade-in {
    from {
        opacity: 0;
    }

    to {
        opacity: 100;
    }
}
</style>