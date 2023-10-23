<script setup lang="ts">
import useFile from '@/composables/useFile';

defineProps<{
    mode: 'new-xweet' | 'modal-new-xweet' | 'edit-xweet' | 'reply-xweet'
    submitFunc: () => Promise<void>
    isLoading: boolean
    isSuccess: boolean
    charCount: number
    maxCharCount: number
    media?: string
}>()
const emit = defineEmits<{
    (e: 'set-media', fileUrl: string): void
}>()

const modeMap = {
    'new-xweet': {
        btn: 'Xweet',
        tooltip: 'Add new xweet',
        successMsg: 'You posted a new xweet!'
    },
    'modal-new-xweet': {
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

const addFile = async (e: Event) => {
    const file =  await useFile(e)
    if (file) {
        emit('set-media', file)
    }
}

const removeFile = () => {
    emit('set-media', '')
}
</script>

<template>
    <div class="w-full py-4 flex justify-between items-start">
        <div class="flex items-center gap-2 h-full">
            <label :for="`${mode}-add-image`" title="Add image to your xweet">
                <span
                    class="flex items-center gap-2 px-2 py-1 bg-sky-800/50 text-xs text-white rounded-md transition-colors cursor-pointer hover:bg-sky-800 dark:bg-sky-400/50 dark:hover:bg-sky-400">
                    <font-awesome-icon icon="fa-solid fa-images" />
                    <h6>Image</h6>
                </span>
                <input 
                    type="file" 
                    :id="`${mode}-add-image`" 
                    accept="image/jpeg, image/png" 
                    class="hidden"
                    @change="addFile">
            </label>
            <div v-show="media" class="relative group">
                <img :src="media" class="w-8 h-8 object-scale-down" />
                <font-awesome-icon 
                    icon="fa-regular fa-circle-xmark" 
                    title="Remove the image"
                    class="absolute -top-1 -right-1 text-xs text-sky-800 cursor-pointer dark:text-white hidden group-hover:block"
                    @click.prevent="removeFile" />
            </div>
        </div>
        <div class="flex items-center h-full px-2 text-center dark:text-white">
            <Transition mode="out-in">
                <p v-if="charCount <= maxCharCount && !isSuccess && !isLoading" class="text-xs">
                    <span>{{ charCount }}</span>
                    /
                    <span class="text-sky-800 dark:text-sky-600">{{ maxCharCount }}</span>
                </p>
                <p v-else-if="charCount > maxCharCount" class="text-red-600 fade-in dark:text-red-400">
                    Your xweet exceeds the maximum number of characters
                </p>
                <p v-else-if="isSuccess" class="text-sky-800 font-bold fade-in dark:text-sky-600">
                    {{ modeMap[mode].successMsg }}
                </p>
            </Transition>
        </div>
        <div class="flex items-center gap-2 h-full">
            <font-awesome-icon 
                v-show="isLoading"
                icon="fa-solid fa-spinner" spin-pulse 
                class="text-white" />
            <input 
                type="button" 
                :value="modeMap[mode].btn"
                class="px-4 py-1 bg-sky-600 text-white font-semibold rounded-md transition-colors duration-200 cursor-pointer hover:bg-sky-800 active:shadow-inner disabled:bg-slate-800 disabled:text-slate-600 disabled:cursor-not-allowed"
                :disabled="charCount > maxCharCount || (charCount === 0 && !media) || isLoading" 
                :title="modeMap[mode].tooltip" 
                @mousedown.prevent="submitFunc">
        </div>
    </div>
</template>

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.2s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>