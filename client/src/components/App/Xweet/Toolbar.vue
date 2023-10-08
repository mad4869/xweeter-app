<script setup lang="ts">
import { ref } from 'vue';

defineProps<{
    mode: 'new-xweet' | 'edit-xweet' | 'reply-xweet'
    submitFunc: () => Promise<void>
    isLoading: boolean
    isSuccess: boolean
    showMediaPreview: boolean
    charCount: number
    maxCharCount: number
}>()
const emit = defineEmits<{
    (e: 'send-file', fileUrl: string): void
}>()

const modeMap = {
    'new-xweet': {
        btn: 'Xweet',
        tooltip: 'Add new xweet',
        successMsg: 'You posted a new xweet!'
    },
    'edit-xweet': {
        btn: 'Fix Xweet',
        tooltip: 'Fix your xweet',
        successMsg: 'You fixed your xweet!'
    },
    'reply-xweet': {
        btn: 'Reply',
        tooltip: 'Send reply to the xweet above',
        successMsg: 'You replied to the xweet!'
    }
}

const fileUrl = ref('')

const addFile = (e: Event) => {
    const target = e.target as HTMLInputElement
    const file = target.files?.[0]

    if (file) {
        const reader = new FileReader()

        reader.onload = (e: ProgressEvent<FileReader>) => {
            if (e.target instanceof FileReader) {
                fileUrl.value = e.target.result as string
                emit('send-file', fileUrl.value)
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
            <div v-if="fileUrl && showMediaPreview" class="relative group">
                <img :src="fileUrl" class="w-8 h-8 object-scale-down" />
                <font-awesome-icon 
                    icon="fa-regular fa-circle-xmark" 
                    title="Remove the image"
                    class="absolute -top-1 -right-1 text-xs text-sky-800 cursor-pointer dark:text-white hidden group-hover:block"
                    @click.prevent="removeFile" />
            </div>
        </div>
        <div class="flex items-center h-full px-2 text-center dark:text-white">
            <p class="text-xs" v-if="charCount > maxCharCount && !isSuccess && !isLoading">
                <span>{{ charCount }}</span>
                /
                <span class="text-sky-800 dark:text-sky-600">{{ maxCharCount }}</span>
            </p>
            <p class="text-red-600 opacity-0 fade-in dark:text-red-400" v-if="charCount > maxCharCount">
                Your xweet exceeds the maximum number of characters
            </p>
            <p class="text-sky-800 font-bold opacity-0 fade-in dark:text-sky-600" v-if="isSuccess">
                {{ modeMap[mode].successMsg }}
            </p>
        </div>
        <div class="flex items-center gap-2 h-full">
            <font-awesome-icon 
                v-if="isLoading"
                icon="fa-solid fa-spinner" spin-pulse 
                class="text-white" />
            <input 
                type="button" 
                :value="modeMap[mode].btn"
                class="px-4 py-1 bg-sky-600 text-white font-semibold rounded-md transition-colors duration-200 cursor-pointer hover:bg-sky-800 active:shadow-inner disabled:bg-slate-800 disabled:text-slate-600 disabled:cursor-not-allowed"
                :disabled="charCount > maxCharCount || (charCount === 0 && !fileUrl) || isLoading" 
                :title="modeMap[mode].tooltip" 
                @mousedown.prevent="submitFunc">
        </div>
    </div>
</template>