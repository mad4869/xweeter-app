<script setup lang="ts">
import { computed, ref } from 'vue';

import useAuth from '../../composables/useAuth';
import socket from '../../utils/socket';
import { sendReqCookie } from '../../utils/axiosInstances';
import { XweetResponse } from '../../types/xweets'

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
            socket.emit('timeline', authStore.getSignedInUserId)

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

const manageFile = (e: Event) => {
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
</script>

<template>
    <section class="px-12 flex flex-col justify-between items-center border border-solid border-sky-800 rounded-xl group">
        <span class="w-full py-4 text-2xl text-sky-950 dark:text-white">New Xweet</span>
        <textarea name="new-tweet" id="new-tweet" placeholder="Tell them what have you been up to..." spellcheck="false"
            v-model="body"
            class="w-full h-10 px-4 py-2 bg-sky-200 rounded-lg caret-sky-800 resize-none transition-[height] duration-300 ease-out placeholder:text-sky-400 focus:h-32 focus:outline-none dark:bg-slate-200 dark:placeholder:text-slate-400"
            :class="charCount > MAX_CHARS ? 'text-red-600 focus-visible:outline-red-600' : 'text-slate-700 focus-visible:outline-sky-600'">
        </textarea>
        <div class="w-full py-4 flex justify-between items-start">
            <div class="flex items-center gap-1 h-full">
                <label for="add-image" title="Add image to your xweet">
                    <span
                        class="px-2 py-1 bg-slate-800/50 text-xs text-white rounded-md cursor-pointer hover:bg-slate-800 dark:bg-slate-400/50 dark:hover:bg-slate-400">
                        Add Image
                    </span>
                    <input type="file" id="add-image" alt="Add Image" accept="image/jpeg, image/png" class="hidden"
                        @change="manageFile">
                </label>
                <img :src="fileUrl" class="w-8 h-8 object-scale-down" v-if="fileUrl" />
            </div>
            <div class="flex items-center h-full dark:text-white">
                <p class="text-xs" v-if="charCount <= MAX_CHARS && !isSuccess && !isLoading">
                    <span>{{ charCount }}</span>
                    /
                    <span class="text-sky-800 dark:text-sky-600">{{ MAX_CHARS }}</span>
                </p>
                <p class="text-red-600 opacity-0 fade-in dark:text-red-400" v-if="charCount > MAX_CHARS">
                    Your xweet exceeds the maximum number of characters
                </p>
                <p class="text-sky-800 font-bold opacity-0 fade-in dark:text-sky-600" v-if="isSuccess">
                    You posted a new xweet!
                </p>
            </div>
            <div class="flex items-center gap-2">
                <font-awesome-icon icon="fa-solid fa-spinner" spin-pulse class="text-white" v-if="isLoading" />
                <input type="button" value="Xweet"
                    class="px-4 py-1 bg-sky-600 text-white font-semibold rounded-md transition-colors duration-200 cursor-pointer hover:bg-sky-800 active:shadow-inner disabled:bg-slate-200 disabled:cursor-not-allowed"
                    :disabled="charCount > MAX_CHARS || isLoading" title="Add new xweet" @click.prevent="addXweet">
            </div>
        </div>
    </section>
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